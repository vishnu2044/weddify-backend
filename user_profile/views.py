from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, ProfileSerializer, UserDetailsSeriallzer, UserProfessionalDetailsSeriallzer, UserReligionalDetailsSeriallzer
from user_accounts.models import UserProfile
from .models import UserBasicDetails, ProfessionalDetails, ReligionalDetails, UserBlockedList
from user_preferences.views import auto_add_basic_preferences, auto_update_professional_preference, auto_update_religional_preferences
import time
from datetime import datetime



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
    try:
        user_profile = UserProfile.objects.get(user = user)
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

    except UserProfile.DoesNotExist:
        return Response(data = {"error": "user profile is not completed ! "}, status= status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_blocked_matches(request):
    user = request.user
    try:
        blocked_users = UserBlockedList.objects.filter(user = user)
        user_ids = [blocked_user.blocked_user.id for blocked_user in blocked_users]
        users_data = User.objects.filter(id__in=user_ids)
        serializer = UserSerializer(users_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserBlockedList.DoesNotExist:
        return Response(data={'message': ' no matches are blocked'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def unblock_match(request, match_id):
    user = request.user
    try:
        blocked_user = UserBlockedList.objects.filter(user = user, blocked_user = match_id)
        blocked_user.delete()
        return Response(data={'message': 'match profile unblocked successfully !'}, status=status.HTTP_200_OK)
    except UserBlockedList.DoesNotExist:
        return Response(data={'message': 'The match profile is not present in the blocked list !'}, status=status.HTTP_200_OK)
    


@api_view(['PATCH'])
def UpdateUserProfile(request):
    user = request.user
    
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    user_unique_id = unique_user_id_generator(request)

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
    user_age = calculate_age_profile(date_of_birth)

    if user_age < 18 :
        return Response({'error' : "your age must me minimum 18 years!"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    if serializer.is_valid():
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
        return Response(data = {'error': "serilaizer is not valid "}, status=status.HTTP_400_BAD_REQUEST)
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
            "location": basic_details.location,
            "citizenship": basic_details.citizenship,

        }
        return Response(data, status=status.HTTP_200_OK)
    except UserBasicDetails.DoesNotExist:
        return Response({'message' : "user didnt added user basic details !"}, status=status.HTTP_200_OK)



@api_view(['PATCH'])
def update_basic_details(request):
    user = request.user

    try:
        basic_details = UserBasicDetails.objects.get(user=user)
    except UserBasicDetails.DoesNotExist:
        basic_details = UserBasicDetails.objects.create(user=user)
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response(data={'error' : 'complete user profile first'}, status= status.HTTP_400_BAD_REQUEST)
    if user_profile:
        date_of_birth = user_profile.date_of_birth
        if date_of_birth :
            user_age = calculate_age_basic_details(date_of_birth)
            serializer = UserDetailsSeriallzer(instance=basic_details, data=request.data, context={'user_age': user_age}, partial=True)
        else:
            return Response(data={'error' : 'Update your user profile first!'}, status= status.HTTP_400_BAD_REQUEST)
    else:
        serializer = UserDetailsSeriallzer(instance=basic_details, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        auto_add_basic_preferences(request) 
        data = serializer.data
    else:
        data = serializer.errors
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
        return Response({'message' : "user didnt added user professional details !"}, status=status.HTTP_200_OK)
    
@api_view(['PATCH'])
def update_professional_data(request):
    user = request.user

    try:
        professional_details = ProfessionalDetails.objects.get(user = user)

    except ProfessionalDetails.DoesNotExist:
        professional_details = ProfessionalDetails.objects.create(user = user)

    
    serializer = UserProfessionalDetailsSeriallzer(instance = professional_details, data = request.data,  partial=True)

    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        auto_update_professional_preference(request)
    else:
        data = serializer.errors

    
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_religional_details(request):
    user = request.user

    try:
        religional_details = ReligionalDetails.objects.get(user = user)

        data = {
            "religion": religional_details.religion,
            "caste": religional_details.caste,
            "star": religional_details.star,

        }
        return Response(data)

    except ReligionalDetails.DoesNotExist:
        return Response({'error' : "user didnt added user preligional details !"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_religional_data(request):
    user = request.user
    try:
        religional_details = ReligionalDetails.objects.get(user = user)

    except ReligionalDetails.DoesNotExist:
        religional_details = ReligionalDetails.objects.create(user = user)
    serializer = UserReligionalDetailsSeriallzer(instance = religional_details, data = request.data,  partial=True)
    if serializer.is_valid():
        serializer.save()
        auto_update_religional_preferences(request)
        data = serializer.data
    else:
        data = serializer.errors
    return Response(data)
