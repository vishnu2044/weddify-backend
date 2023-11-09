from django.contrib.auth.models import User
from rest_framework import serializers
from . import models 
from user_accounts.models import UserProfile
from user_profile.models import UserBasicDetails, ProfessionalDetails, ReligionalDetails

class UserMatchesSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    
    profile_img = serializers.SerializerMethodField()
    occupation = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username','id', 'first_name', 'last_name', 'age', 'profile_img' , 'occupation', 'gender')
    
    def get_age(self, obj):
        try:
            data = UserBasicDetails.objects.get(user = obj)
            return data.age
        except UserBasicDetails.DoesNotExist:
            return None 
    
    def get_profile_img(self, obj):
        try:
            data = UserProfile.objects.get(user=obj)
            return data.profile_img.url
        except UserProfile.DoesNotExist:
            return None  
        
    def get_occupation(self, obj):
        try:
            data = ProfessionalDetails.objects.get(user=obj)
            return data.occupation
        except ProfessionalDetails.DoesNotExist:
            return None  
        
    def get_gender(self, obj):
        try:
            data = UserProfile.objects.get(user=obj)
            return data.gender
        except ProfessionalDetails.DoesNotExist:
            return None  



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserBasicDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBasicDetails
        fields = '__all__'

class ProfessionalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalDetails
        fields = '__all__'

class ReligionalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligionalDetails
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


        