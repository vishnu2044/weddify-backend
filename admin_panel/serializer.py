from rest_framework import serializers
from django.contrib.auth.models import User
from user_accounts.models import UserProfile, PremiumVersion
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
        
class PremiumUserSerializer(serializers.ModelSerializer):

    profile_img = serializers.SerializerMethodField()
    plan_name = serializers.SerializerMethodField()
    amount_paid = serializers.SerializerMethodField()
    expiry_date = serializers.SerializerMethodField()
    unique_user_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'id', 'first_name', 'last_name', 'profile_img','plan_name','unique_user_id', 'amount_paid', 'expiry_date' )

    def get_profile_img(request, obj):
        try:
            data = UserProfile.objects.get(user = obj)
            if data.profile_img:
                return data.profile_img.url
            else:
                return None
        except UserProfile.DoesNotExist:
            return None

    def get_unique_user_id(request, obj):
        try:
            data = UserProfile.objects.get(user = obj)
            if data.unique_user_id:
                return data.unique_user_id
            else:
                return None
        except UserProfile.DoesNotExist:
            return None
        
    def get_plan_name(request, obj):
        try:
            data = PremiumVersion.objects.get(user = obj)
            if data.plan_name:
                return data.plan_name
            else:
                return None
        except PremiumVersion.DoesNotExist:
            return None
    
    def get_amount_paid(request, obj):
        try:
            data = PremiumVersion.objects.get(user = obj)
            if data.amount_paid:
                return data.amount_paid
            else:
                return None
        except PremiumVersion.DoesNotExist:
            return None
    
    def get_expiry_date(request, obj):
        try:
            data = PremiumVersion.objects.get(user = obj)
            if data.expiry_date:
                return data.expiry_date
            else:
                return None
        except PremiumVersion.DoesNotExist:
            return None
