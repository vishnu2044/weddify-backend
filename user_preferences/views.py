from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import BasicPreferences, ProfessionalPreferences, ReligionalPreferences
from rest_framework.response import Response
from rest_framework import status
from .serializers import BasicPreferencesSerialzer, ProfessionalPreferenceSerializer, ReligiounalPreferenceSerializer
from user_accounts.models import UserProfile
from user_profile.models import UserBasicDetails, ProfessionalDetails, ReligionalDetails

# Create your views here.

##############################################################################
##############################################################################
# here user basic preference auto added when user add basic details.##########
##############################################################################
##############################################################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_basic_preferences(request):
    user = request.user
    try:
        basic_preferences = BasicPreferences.objects.get(user = user)
        
        data = {
            "age_to": basic_preferences.age_to,
            "age_from": basic_preferences.age_from,
            "mother_tongue": basic_preferences.mother_tongue,
            "eating_habit": basic_preferences.eating_habit,
            "drinking_habit": basic_preferences.drinking_habit,
            "smoking_habit": basic_preferences.smoking_habit,
            "martial_status": basic_preferences.martial_status,
            "height": basic_preferences.height,
            "body_type": basic_preferences.body_type,
            "physical_status": basic_preferences.physical_status,
            "location": basic_preferences.location,
            "citizenship": basic_preferences.citizenship,

        }
        return Response(data)
    except BasicPreferences.DoesNotExist:
        return Response({'error' : "user didnt added user profile details !"}, status=status.HTTP_400_BAD_REQUEST)



def auto_add_basic_preferences(request):
    user = request.user
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    
    basic_preferences = BasicPreferences.objects.filter(user=user).first()
    if basic_preferences:
        print("table is already created !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return
        
    else:
        print("auto add user basic preferences !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        basic_preferences = BasicPreferences.objects.create(user=user)

    try:
        user_profile = UserProfile.objects.get(user=user)
        user_basic_details = UserBasicDetails.objects.get(user=user)

        if user_profile.gender == 'male':
            basic_preferences.gender = 'female'
            basic_preferences.age_from = 18
            basic_preferences.age_to = user_basic_details.age
        else:
            basic_preferences.gender = 'male'
            basic_preferences.age_from = user_basic_details.age
            basic_preferences.age_to = user_basic_details.age + 5

        basic_preferences.mother_tongue = user_basic_details.mother_tongue
        basic_preferences.eating_habit = user_basic_details.eating_habit
        basic_preferences.drinking_habit = user_basic_details.drinking_habit
        basic_preferences.smoking_habit = user_basic_details.smoking_habit
        basic_preferences.martial_status = user_basic_details.martial_status
        basic_preferences.height = user_basic_details.height
        basic_preferences.body_type = user_basic_details.body_type
        basic_preferences.physical_status = user_basic_details.physical_status
        basic_preferences.location = user_basic_details.location
        basic_preferences.citizenship = user_basic_details.citizenship
        basic_preferences.save()
    except (UserProfile.DoesNotExist, UserBasicDetails.DoesNotExist):
        print("got an error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return Response({'message': "basic details or user profile is not created."})
    return Response({'message': "Basic preferences updated successfully."})



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_basic_preferences(request):
    print("basic preference called !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user = request.user
    try:
        basic_details =  BasicPreferences.objects.get(user = user)
    except BasicPreferences.DoesNotExist:
        basic_details = BasicPreferences.objects.create(user=user)

    serializer = BasicPreferencesSerialzer(instance=basic_details, data=request.data,  partial=True)



    if serializer.is_valid():
        print(":::::::::::::::::::::::   basic details serializer is valid ::::::::::::::::::::::::::::::")
        serializer.save()
        data = serializer.data
        print("serializer data ::::::::::::::::::::::::::::::::::", data)
    else:
        data = serializer.errors
        print("basic details serializer is not working  error ::::::::::::::::", data)
    return Response(data)



##############################################################################
##############################################################################
# here user Professional preference auto added when user add basic details.###
##############################################################################
##############################################################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_professional_preferences(request):
    user = request.user
    try:
        professional_preference = ProfessionalPreferences.objects.get(user=user)
        data = {
            'education' : professional_preference.education,
            'college': professional_preference.college,
            'working_sector': professional_preference.working_sector,
            'income': professional_preference.income,
            'occupation' : professional_preference.occupation,
            'organization' : professional_preference.organization,
            'working_location' : professional_preference.working_location,
            
        }
        return Response(data)
    
    except ProfessionalPreferences.DoesNotExist:
        return Response({'message' : "user didnt added user profile details !"}, status=status.HTTP_200_OK)



def auto_update_professional_preference(request):
    print("auto update called !!!!!!!!!!!!!!!!")
    user = request.user

    try:
        professional_preference = ProfessionalPreferences.objects.get(user=user)
        print("Professional preferences already exist")
        return
    except ProfessionalPreferences.DoesNotExist:
        professional_preference = ProfessionalPreferences.objects.create(user=user)
        print("Professional preferences created")

    try:
        professional_data = ProfessionalDetails.objects.get(user=user)

        professional_preference.education = professional_data.education
        professional_preference.college = 'any'
        professional_preference.working_sector = professional_data.working_sector
        professional_preference.income = professional_data.income
        professional_preference.occupation = professional_data.occupation
        professional_preference.organization = 'any'
        professional_preference.working_location = 'any'
        professional_preference.save()
        print("Professional preferences updated")

    except ProfessionalDetails.DoesNotExist:
        print("Auto update error: user didn't add professional details")
        return Response({'error': "User didn't add professional details!"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH']) 
@permission_classes([IsAuthenticated])
def update_prfessional_preference(request):
    print("basic preference called !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user = request.user
    try:
        professional_preferences =  ProfessionalPreferences.objects.get(user = user)
    except ProfessionalPreferences.DoesNotExist:
        professional_preferences = ProfessionalPreferences.objects.create(user=user)

    serializer = ProfessionalPreferenceSerializer(instance=professional_preferences, data=request.data,  partial=True)

    if serializer.is_valid():
        print(":::::::::::::::::::::::   professional preference serializer is valid ::::::::::::::::::::::::::::::")
        serializer.save()
        data = serializer.data
        print("serializer data ::::::::::::::::::::::::::::::::::", data)
    else:
        data = serializer.errors
        print("basic details serializer is not working  error ::::::::::::::::", data)
    return Response(data)



##############################################################################
##############################################################################
# here user religional preference auto added when user add basic details.#####
##############################################################################
##############################################################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_religious_preferences(reqeust):
    user = reqeust.user

    try:
        religious_preferences = ReligionalPreferences.objects.get(user = user)
        data = {
            'religion' : religious_preferences.religion,
            'caste' : religious_preferences.caste,
            'star' : religious_preferences.star,

        }
        return Response(data)
    
    except ReligionalPreferences.DoesNotExist:
        return Response({'message' : "user didnt added user profile details !"}, status=status.HTTP_200_OK)
    
def auto_update_religional_preferences(request):
    user = request.user
    try:
        religional_preference = ReligionalPreferences.objects.get(user=user)
        print("Professional preferences already exist")
        return
    except ReligionalPreferences.DoesNotExist:
        religional_preference = ReligionalPreferences.objects.create(user=user)
        print("Professional preferences created")

    try:
        religional_data = ReligionalDetails.objects.get(user=user)

        religional_preference.religion = religional_data.religion
        religional_preference.caste = religional_data.caste
        religional_preference.star = 'any'


        religional_preference.save()
        print("Professional preferences updated")

    except ReligionalDetails.DoesNotExist:
        print("Auto update error: user didn't add rligiounal details")
        return Response({'error': "User didn't add religiounal details!"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PATCH']) 
@permission_classes([IsAuthenticated])
def update_religiounal_preference(request):
    print("basic preference called !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user = request.user
    try:
        religional_preferences =  ReligionalPreferences.objects.get(user = user)
        print("religios preference table get !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    except ReligionalPreferences.DoesNotExist:
        religional_preferences = ReligionalPreferences.objects.create(user=user)
        print("religios preference table created !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    serializer = ReligiounalPreferenceSerializer(instance=religional_preferences, data=request.data,  partial=True)

    if serializer.is_valid():
        print(":::::::::::::::::::::::   religious preference serializer is valid ::::::::::::::::::::::::::::::")
        serializer.save()
        data = serializer.data
        print("serializer data ::::::::::::::::::::::::::::::::::", data)
    else:
        data = serializer.errors
        print("basic details serializer is not working  error ::::::::::::::::", data)
    return Response(data)