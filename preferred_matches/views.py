from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserMatchesSerializer, UserSerializer, ProfessionalDetailsSerializer, ReligionalDetailsSerializer, UserBasicDetailsSerializer, UserProfileSerializer, UserVisitedProfiles, VisitedMatchesProfiles
from rest_framework import status
from user_profile.models import UserBasicDetails, ProfessionalDetails, ReligionalDetails, UserBlockedList, ProfileVisitedUsers, ProfileLikeList
from user_preferences.models import BasicPreferences, ReligionalPreferences, ProfessionalPreferences
from user_accounts.models import UserProfile
from datetime import datetime, timedelta
# Create your views here.


def get_matches(request):
    user = request.user
    userlist = User.objects.all().exclude(is_superuser=True).exclude(id=user.id)
    try:
        try:
            blocked_list = UserBlockedList.objects.filter(user= user)
            blocked_user_ids = blocked_list.values_list('blocked_user__id', flat=True)
            userlist = userlist.exclude(id__in = blocked_user_ids)
        except UserBlockedList.DoesNotExist:
            print("user block list not excits!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
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
    except UserBasicDetails.DoesNotExist:
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
    
    serializer = UserMatchesSerializer(user_list, many=True, context={'request': request})
    print("all data ::::::::::::::::::::::::::::::: like :::::::::::::::::::::",serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_matches(request):
    current_user = request.user
    user_list = get_matches(request) 
    current_time = datetime.now()
    twelve_hours_ago = current_time - timedelta(days=4)
    user_list = user_list.filter(date_joined__gte=twelve_hours_ago)
    serializer = UserMatchesSerializer(user_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_match_profile(request, match_id):
    current_user = request.user
    
    try:
        user = User.objects.get(id=match_id)
        data = {}

        user_serializer = UserSerializer(user)
        data['user'] = user_serializer.data

        try:
            profile_visited_list = ProfileVisitedUsers.objects.get(user = current_user, visited_profile = user)
            profile_visited_list.visited_time = datetime.now()
            profile_visited_list.save()
        except ProfileVisitedUsers.DoesNotExist:
            # The visited profile does not exist in the database, so create a new record.
            profile_visited_list = ProfileVisitedUsers.objects.create(user = current_user, visited_profile = user)
        profile_visited_list.save()

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
       
        return Response(data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User doesn't exist!!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def block_user(request, block_user):
    user = request.user
    try:
        blocked_user = User.objects.get(id = block_user)

        excisting_user = UserBlockedList.objects.filter(user=user, blocked_user=blocked_user)
        if not excisting_user:
            UserBlockedList.objects.create(user=user, blocked_user=blocked_user)
        return Response(data={'message': 'success'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        print("didnt get the profile!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response(data={'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def like_match(request, match_id):
    current_user = request.user
    
    try:
        liked_user = User.objects.get(id=match_id)

        profile_like = ProfileLikeList.objects.filter(user=current_user, liked_profile=liked_user)

        if not profile_like.exists():
            ProfileLikeList.objects.create(user=current_user, liked_profile=liked_user)
            return Response(data={'message': "user liked the match"}, status=status.HTTP_200_OK)
        
        else:
            print("User has already liked the match")
            return Response(data={'message': "user has already liked the match"}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response(data={'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def unlike_match(request, match_id):
    current_user = request.user
    try:
        liked_user = User.objects.get(id = match_id)
        profile_like = ProfileLikeList.objects.filter(user = current_user, liked_profile = liked_user)
        profile_like.delete()
        return Response(data={'message': "user unliked your profile"}, status=status.HTTP_200_OK)
    except ProfileLikeList.DoesNotExist:
        return Response(data={'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewed_profiles(request):
    current_user = request.user

    try:
        visited_profiles = ProfileVisitedUsers.objects.filter(user = current_user)

        # Serialize the list of visited profiles
        visited_profile_ids = [visited_profile.visited_profile.id for visited_profile in visited_profiles]

        visited_profile_data = User.objects.filter(id__in = visited_profile_ids)
        print("users data ::::::::::::::::::::::::::::::::::::::::::::::::::::", visited_profile_data)
        serializer = UserVisitedProfiles(visited_profile_data, many=True,  context={'request': request})
        print('seralized data :::::::::::::::::::::::::::::::', serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except ProfileVisitedUsers.DoesNotExist:
        return Response({'error': "User didn't visit any profiles!"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matches_viewed_yours(request):
    current_user = request.user

    try:
        visited_matches = ProfileVisitedUsers.objects.filter(visited_profile = current_user)
        visited_match_ids = [visited_match.user.id for visited_match in visited_matches]
        count = 0
        for x in visited_match_ids:
            print("visited profiles id ::::::::", x)
            count +=1
        visited_matches_data = User.objects.filter(id__in = visited_match_ids)

        serialzer = VisitedMatchesProfiles(visited_matches_data, many=True, context={'request': request})
        data = serialzer.data
        additional_data = {'match_count': count}
        response_data = {'data' : data, **additional_data}
        return Response(response_data, status=status.HTTP_200_OK)
    except ProfileVisitedUsers.DoesNotExist:
        return Response({'error': "User didn't visit any profiles!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_profile_completed(request):
    current_user = request.user
    try:
        userprofile = UserProfile.objects.get(user = current_user)
        if userprofile.unique_user_id == None:
            print("profile is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    except UserProfile.DoesNotExist:
        print("UserProfile is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete your User profile !"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        UserBasicDetails.objects.get(user = current_user)
        print('basic details completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except UserBasicDetails.DoesNotExist:
        print("UserBasicDetails is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete your basic details !"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ProfessionalDetails.objects.get(user = current_user)
        print('basic details completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except ProfessionalDetails.DoesNotExist:
        print("ProfessionalDetails is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete your professional details !"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ReligionalDetails.objects.get(user = current_user)
        print('basic details completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except ReligionalDetails.DoesNotExist:
        print("ReligionalDetails is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete your religional details !"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        BasicPreferences.objects.get(user = current_user)
        print('basic preferences completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except BasicPreferences.DoesNotExist:
        print("basic preferences is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete yourbasic preferences !"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ProfessionalPreferences.objects.get(user = current_user)
        print('professional preferences completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except ProfessionalPreferences.DoesNotExist:
        print("basic preferences is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete your professional preferences !"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        ReligionalPreferences.objects.get(user = current_user)
        print('professional preferences completed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except ReligionalPreferences.DoesNotExist:
        print("professional preferences is not completed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'error': "please complete your religional preferences !"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(data = {"message" : "success"}, status=status.HTTP_200_OK)