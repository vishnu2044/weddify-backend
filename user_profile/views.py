from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, UserDetailsSeriallzer
from user_accounts.models import UserProfile
from .models import UserBasicDetails


from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user

    serializer = UserSerializer(user)

    user_profile = get_object_or_404(UserProfile, user=user)

    user_profile_data = {
        'unique_user_id': user_profile.unique_user_id,
        'profile_img': user_profile.profile_img.url if user_profile.profile_img else '',
        'phone_number': user_profile.phone_number,
        'date_of_birth': user_profile.date_of_birth,
        'gender': user_profile.gender,
    }

    data = {
        'response': 'registered',
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_profile': user_profile_data,
    }

    return Response(data)


@api_view(['PATCH'])
def UpdateUserProfile(request):
    print("update profile called !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user = request.user
    print("the user !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", user)

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    print("user data ::::::::::", request.data)
    if 'profile_img' in request.FILES:
        profile.profile_img = request.FILES['profile_img']

    serializer = ProfileSerializer(instance = profile, data=request.data, partial=True )

    new_username = request.data.get('username', user.username)
    if user.username != new_username and User.objects.filter(username = new_username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    new_email = request.data.get('email', user.email)
    if user.email != new_email and User.objects.filter(email = new_email).exists():
        return Response({'error' : "email is already exists!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    if serializer.is_valid():
        print("serializer is validddd !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        serializer.save()
        data = serializer.data
        user.username = request.data.get('username', user.username)
        user.mail = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()

        data['response'] = 'registered'
        data['username'] = user.username
        data['email'] = user.email
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
    else:
        data = serializer.errors
        print("profile updated is not working !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", serializer.errors)
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_basic_details(request):
    user = request.user
    try:
        basic_details = UserBasicDetails.objects.get(user = user)
    except UserBasicDetails.DoesNotExist:
        return Response({'error' : "user didnt added user basic details !"}, status=status.HTTP_400_BAD_REQUEST)




def update_basic_details(request):
    user = request.user
    try:
        basic_details =  UserBasicDetails.ojbects.get(user = user)
    except UserBasicDetails.DoesNotExist:
        profile = UserBasicDetails.objects.create(user=user)

    serializer = UserDetailsSeriallzer(instance = profile, data=request.data, user=user, partial=True )









