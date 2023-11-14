from django.contrib.auth.models import User
from rest_framework import serializers
from . import models 
from user_accounts.models import UserProfile
from user_profile.models import UserBasicDetails, ProfessionalDetails, ReligionalDetails, ProfileVisitedUsers, ProfileLikeList
from datetime import datetime, timezone
from user_preferences.models import BasicPreferences, ProfessionalPreferences, ReligionalPreferences

class UserMatchesSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()
    occupation = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'age', 'profile_img' , 'occupation', 'gender', 'like')
    
    def get_age(self, obj):
        try:
            data = UserBasicDetails.objects.get(user = obj)
            return data.age
        except UserBasicDetails.DoesNotExist:
            return None 
    
    def get_like(self, obj):
        request = self.context.get('request')
        if request:
            try:
                data = ProfileLikeList.objects.get(user=request.user, liked_profile=obj)
                if data:
                    return True
            except ProfileLikeList.DoesNotExist:
                return False
        else:
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
        except  UserProfile.DoesNotExist:
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


class UserVisitedProfiles(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    visited_time = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_img', 'visited_time', 'id')
    
    def get_profile_img(self, obj):
        try:
            data = UserProfile.objects.get(user=obj)
            return data.profile_img.url
        except UserProfile.DoesNotExist:
            return None  

    def get_visited_time(self, obj):
        current_user = self.context['request'].user

        try:
            data = ProfileVisitedUsers.objects.get(user=current_user, visited_profile=obj)
            activity_time = data.visited_time

            # Calculate the time difference
            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            time_difference = current_time - activity_time
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            # Format the result
            if days > 0:
                return f"{days} {'day' if days == 1 else 'days'} ago"
            elif hours > 0:
                return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
            elif minutes > 0:
                return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
            else:
                return "Just now"

        except ProfileVisitedUsers.DoesNotExist:
            return None


class VisitedMatchesProfiles(serializers.ModelSerializer):
    profile_img = serializers.SerializerMethodField()
    visited_time = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'profile_img', 'visited_time', 'id')
    
    def get_profile_img(self, obj):
        try:
            data = UserProfile.objects.get(user=obj)
            return data.profile_img.url
        except UserProfile.DoesNotExist:
            return None  

    def get_visited_time(self, obj):
        current_user = self.context['request'].user

        try:
            data = ProfileVisitedUsers.objects.get(user=obj, visited_profile=current_user)
            activity_time = data.visited_time

            # Calculate the time difference
            current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
            time_difference = current_time - activity_time
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, _ = divmod(remainder, 60)

            # Format the result
            if days > 0:
                return f"{days} {'day' if days == 1 else 'days'} ago"
            elif hours > 0:
                return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
            elif minutes > 0:
                return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
            else:
                return "Just now"

        except ProfileVisitedUsers.DoesNotExist:
            return None


class BasicPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPreferences
        fields = ('age_from', 'age_to', 'martial_status', 'location')


class ProfessionalPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessionalPreferences
        fields = ('working_sector', 'occupation')


class ReligionalPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligionalPreferences
        fields = ('religion', 'caste')
