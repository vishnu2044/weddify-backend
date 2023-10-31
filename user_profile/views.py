from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, UserDetailsSeriallzer, UserProfessionalDetailsSeriallzer
from user_accounts.models import UserProfile
from .models import UserBasicDetails, ProfessionalDetails

import time
from datetime import datetime, date

from django.shortcuts import get_object_or_404

def unique_user_id_generator(request):
    user = request.user

    date_joined_str = user.date_joined.strftime("%Y%m%d")[-4:]
    first_name = user.first_name[:3].upper()
    site_name = 'WED'
    current_time = str(time.time())

    user_unique_id = f'{site_name}{first_name.upper()}{date_joined_str}T{current_time[:3]}'
    return user_unique_id


def calculate_age_profile(date_of_birth):
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
    current_date = datetime.now().date()
    age = current_date.year - date_of_birth.year 
    return age

def calculate_age_basic_details(date_of_birth):
    current_date = datetime.now().date()
    age = current_date.year - date_of_birth.year - ((current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day))
    return age


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
    
    user = request.user
    print("the user ::::::::::::::::::::::::::::::::::::::::", user)

    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    user_unique_id = unique_user_id_generator(request)
    print("user unique id ::::::::::::::::::::::::::::::::::::::::::::::::::::",user_unique_id)

    print("user data ::::::::::", request.data)
    if 'profile_img' in request.FILES:
        profile.profile_img = request.FILES['profile_img']

    serializer = ProfileSerializer(instance = profile, data=request.data, context={'user_unique_id': user_unique_id}, partial=True )

    new_username = request.data.get('username', user.username)
    if user.username != new_username and User.objects.filter(username = new_username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    new_email = request.data.get('email', user.email)
    if user.email != new_email and User.objects.filter(email = new_email).exists():
        return Response({'error' : "email is already exists!"}, status=status.HTTP_400_BAD_REQUEST)
    
    date_of_birth = request.data.get('date_of_birth')
    print("date of birth ::::::::::::::::::::::::::::::::::::::::::::", date_of_birth)
    user_age = calculate_age_profile(date_of_birth)
    print("user age ::::::::::::::::::::::::::::::::::::::::::::", user_age)
    if user_age < 18 :
        return Response({'error' : "your age must me minimum 18 years!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
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
        data = {
            "age": basic_details.age,
            "mother_tongue": basic_details.mother_tongue,
            "eating_habit": basic_details.eating_habit,
            "drinking_habit": basic_details.drinking_habit,
            "smoking_habit": basic_details.smoking_habit,
            "martial_status": basic_details.martial_status,
            "height": basic_details.height,
            "body_type": basic_details.body_type,
            "physical_status": basic_details.physical_status,

        }
        return Response(data)
    except UserBasicDetails.DoesNotExist:
        return Response({'error' : "user didnt added user basic details !"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PATCH'])
def update_basic_details(request):
    user = request.user
    try:
        basic_details =  UserBasicDetails.objects.get(user = user)
    except UserBasicDetails.DoesNotExist:
        basic_details = UserBasicDetails.objects.create(user=user)
    try:
        user_profile = UserProfile.objects.get(user=user)

    except UserBasicDetails.DoesNotExist:
        print("date not found::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("input data :::::::::::::::::::::::::::::::", request.data)
    print("database :::::::::::::::::::::: ", basic_details)

    if user_profile:
        date_of_birth = user_profile.date_of_birth
        user_age = calculate_age_basic_details(date_of_birth)
        print("date of birth ::::::::::::::::::::::::::::::::::", date_of_birth)
        serializer = UserDetailsSeriallzer(instance=basic_details, data=request.data, context={'user_age': user_age}, partial=True)
    else:
        serializer = UserDetailsSeriallzer(instance=basic_details, data=request.data,  partial=True)



    if serializer.is_valid():
        print(":::::::::::::::::::::::   basic details serializer is valid ::::::::::::::::::::::::::::::")
        serializer.save()
        data = serializer.data
        print("serializer data ::::::::::::::::::::::::::::::::::", data)
    else:
        data = serializer.errors
        print("basic details serializer is not working  error ::::::::::::::::", data)
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_professional_details(request):
    user = request.user

    try:
        professional_details = ProfessionalDetails.objects.get(user = user)

        data = {
            "education": professional_details.education,
            "college": professional_details.college,
            "working_sector": professional_details.working_sector,
            "income": professional_details.income,
            "occupation": professional_details.occupation,
            "organization": professional_details.organization,
        }
        return Response(data)

    except ProfessionalDetails.DoesNotExist:
        return Response({'error' : "user didnt added user professional details !"}, status=status.HTTP_400_BAD_REQUEST)
    

def update_professional_data(request):
    user = request.user

    try:
        professional_details = ProfessionalDetails.objects.get(user = user)
    except UserBasicDetails.DoesNotExist:
        professional_details = ProfessionalDetails.objects.create(user = user)
    
    serializer = UserProfessionalDetailsSeriallzer(instance = professional_details, data = request.data,  partial=True)

    if serializer.is_valid():
        serializer.save()
        print(":::::::::::::::::::  serializer is saved  :::::::::::::::::::::::::::::::::::::::::")
        data = serializer.data
    else:
        data = serializer.errors
        print(":::::::::::::::::::  serializer is failed  :::::::::::::::::::::::::::::::::::::::::")
    
    return Response(data)

