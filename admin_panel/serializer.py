from rest_framework import serializers
from django.contrib.auth.models import User
from user_accounts.models import UserProfile
from .models import PremiumPlans


class UserSerialzer(serializers.ModelSerializer):
    gender = serializers.SerializerMethodField()
    profile_img = serializers.SerializerMethodField()
    unique_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'id', 'gender', 'profile_img', 'email', 'is_active', 'unique_id')

    def get_unique_id(self, object):
        try:
            data = UserProfile.objects.get(user = object)
            return data.unique_user_id
        except UserProfile.DoesNotExist:
            return None
        
    def get_gender(self, object):
        try:
            data = UserProfile.objects.get(user = object)
            return data.gender
        except UserProfile.DoesNotExist:
            return None
        
    def get_profile_img(self, object):
        try:
            data = UserProfile.objects.get(user=object)
            if data.profile_img:
                return data.profile_img.url
            else:
                return None
        except UserProfile.DoesNotExist:
            return None   
        
class PremiumPlanSerilalizer(serializers.ModelSerializer):

    class Meta:
        model = PremiumPlans
        fields = '__all__'
        