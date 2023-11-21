from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import UserSerialzer
from django.contrib.auth.models import AnonymousUser
from .models import PremiumPlans

from preferred_matches.serializers import UserSerializer,  UserBasicDetailsSerializer, UserProfileSerializer, ProfessionalDetailsSerializer, ReligionalDetailsSerializer
from user_profile.models import UserBasicDetails, ProfessionalDetails, ReligionalDetails
from user_accounts.models import UserProfile


class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)

        if user.is_staff:
            token['is_staff'] = True
        return token


@api_view(['POST'])
def admin_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username = username, password = password)
    print("admin user is ", user)

    if user is not None and user.is_superuser:
        serializer = AdminTokenObtainPairSerializer(data = {'username' : username, 'password': password})
        serializer.is_valid(raise_exception=True)
        token_data = serializer.validated_data
        
        return Response({
            'access': token_data['access'],
            'refresh': token_data['refresh'],
            'is_staff': user.is_staff
        })
    else:
        return Response({'error': 'Invalid Credentials'}, status= status.HTTP_401_UNAUTHORIZED)

@api_view(['get'])
@permission_classes([IsAuthenticated])
def check_user_is_admin(request):
    current_user = request.user
    if current_user.is_superuser:
        data = {'check': 'is_admin'}
        
    elif current_user.is_authenticated:
        data = {'check': 'is_normal_user'}
        
    elif isinstance(current_user, AnonymousUser):
        data = {'check': 'not_authenticated'}

    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin_panel_data(request):
    current_user = request.user

    if current_user.is_superuser:
        all_users = User.objects.all().exclude(is_superuser=True)
        total_users = User.objects.all().exclude(is_superuser=True).count()

        men = all_users.filter(userprofile__gender = 'male')
        total_men = all_users.filter(userprofile__gender = 'male').count()

        women = all_users.filter(userprofile__gender = 'female')
        total_women = all_users.filter(userprofile__gender = 'female').count()  

        all_user_serializer = UserSerialzer(all_users, many=True)
        men_serializer = UserSerialzer(men, many=True)
        women_serializer = UserSerialzer(women, many=True)

        response_data = {
            'all_users': all_user_serializer.data,
            'men': men_serializer.data,
            'women': women_serializer.data,
            'total_men' : total_men,
            'total_users' : total_users,
            'total_women': total_women
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
    
    else:
        return Response(data={'error':'fail'}, status=status.HTTP_401_UNAUTHORIZED)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request, profile_id):
    
    try:
        user = User.objects.get(id=profile_id)
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
       
        return Response(data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User doesn't exist!!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_block_management(request, user):
    current_user = request.user
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> u", current_user)
    if current_user.is_superuser:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> user suprer user is checking")
        try:
            print("user ::::::::::::::::::::::::::::::::::>>>>>>>>>>>>>>>>>>>>>>>", user)
            user = User.objects.get(pk=user)
            if user.is_active == True:
                user.is_active = False
                user.save()
                return Response({'success':'user blocked successfully!'}, status=status.HTTP_200_OK)
            else:
                user.is_active =True
                user.save()
                return Response(data = { 'success' : 'user unblocked successfully !'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(data = {"error": "User doesn't exist!!"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error' : 'user is not super user'}, status = status.HTTP_401_UNAUTHORIZED)
        

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def edit_premium_plans(request):
    user = request.user
    if user is not None and user.is_superuser:
        try:
            premium = PremiumPlans.objects.latest('updated_time')
        except PremiumPlans.DoesNotExist:
            premium = PremiumPlans.objects.create()
        
        monthly_price_data = request.data.get('monthly_price')
        yearly_price_data = request.data.get('yearly_price')
        premium.monthly_price = monthly_price_data
        premium.yearly_price = yearly_price_data
        premium.save()
        return Response({'success': 'premium plans updated successfully!!'}, status=status.HTTP_200_OK)
    else:
        return Response(data = {"error": "user is not authenticated!!"}, status=status.HTTP_401_UNAUTHORIZED)
