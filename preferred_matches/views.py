from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserMatchesSerializer, UserSerializer, ProfessionalDetailsSerializer, ReligionalDetailsSerializer, UserBasicDetailsSerializer, UserProfileSerializer
from rest_framework import status
from user_profile.models import UserBasicDetails, ProfessionalDetails, ReligionalDetails
from user_preferences.models import BasicPreferences
from user_accounts.models import UserProfile
from datetime import datetime, timedelta
# Create your views here.


def get_matches(request):
    user = request.user
    userlist = User.objects.all().exclude(is_superuser=True).exclude(id=user.id)
    try:
        basic_preferences = BasicPreferences.objects.get(user=user)
        user_list = userlist.filter(userprofile__gender=basic_preferences.gender)
        print(user_list)
        return user_list
    except BasicPreferences.DoesNotExist:
        return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_matches_location_based(request):
    user = request.user
    user_list = get_matches(request)
    try:
        user_Basic_details = UserBasicDetails.objects.get(user=user)
        userlist = user_list.filter(userbasicdetails__location = user_Basic_details.location)
    except BasicPreferences.DoesNotExist:
        return Response({'error' : "didnt get the user basic preferences !"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserMatchesSerializer(userlist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_matches(request):
    user = request.user
    user_list = get_matches(request)
    try:
        basic_preferences = BasicPreferences.objects.get(user = user)
        user_list = user_list.filter(userbasicdetails__age__gte = basic_preferences.age_from, userbasicdetails__age__lte = basic_preferences.age_to  )
    except BasicPreferences.DoesNotExist:
        return Response({'error' : "didnt get the user basic preferences !"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserMatchesSerializer(user_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_matches(request):
    user_list = get_matches(request) 
    current_time = datetime.now()
    twelve_hours_ago = current_time - timedelta(days=4)
    user_list = user_list.filter(date_joined__gte=twelve_hours_ago)
    serializer = UserMatchesSerializer(user_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_profile(request, match_id):
    print("its works!!!!!!!!!!!!!!!!!!!!!!!!")
    try:
        user = User.objects.get(id=match_id)
        print(user, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        data = {}

        user_serializer = UserSerializer(user)
        data['user'] = user_serializer.data

        try:
            user_basic_details = UserBasicDetails.objects.get(user=user)
            user_basic_details_serializer = UserBasicDetailsSerializer(user_basic_details)
            data['basic'] = user_basic_details_serializer.data
        except UserBasicDetails.DoesNotExist:
            data['basic'] = None

        try:
            user_profile_details = UserProfile.objects.get(user=user)
            user_profile_details_serializer = UserProfileSerializer(user_profile_details)
            data['profile'] = user_profile_details_serializer.data
        except UserBasicDetails.DoesNotExist:
            data['profile'] = None

        try:
            user_professional_details = ProfessionalDetails.objects.get(user=user)
            user_professional_details_serializer = ProfessionalDetailsSerializer(user_professional_details)
            data['professional'] = user_professional_details_serializer.data
        except ProfessionalDetails.DoesNotExist:
            data['professional'] = None

        try:
            user_religional_details = ReligionalDetails.objects.get(user=user)
            user_religional_details_serializer = ReligionalDetailsSerializer(user_religional_details)
            data['religional'] = user_religional_details_serializer.data
        except ReligionalDetails.DoesNotExist:
            data['user_religional_details'] = None
        print(data, "33333333333333333333333333333333333333333333333333333333333333333333333")
        return Response(data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User doesn't exist!!"}, status=status.HTTP_400_BAD_REQUEST)
