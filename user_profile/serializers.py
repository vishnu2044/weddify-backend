from django.contrib.auth.models import User
from rest_framework import serializers
from user_accounts.models import UserProfile
from rest_framework.serializers import ImageField, ValidationError, ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserBasicDetails


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_joined')



class ProfileSerializer(ModelSerializer):
    profile_img = ImageField(read_only = True)
    class Meta:
        model = UserProfile
        fields = '__all__'
    

    def update(self, instance, validated_data):

        # new_phone_number = validated_data.get('phone_number', instance.phone_number)
        # if UserProfile.phone_number != new_phone_number and UserProfile.objects.filter(phone_number = new_phone_number).exists():
        #     return Response({'error' : "phone number is already exists!"}, status=status.HTTP_400_BAD_REQUEST)

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@    serializer udpate  is calling   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(validated_data)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()


        print("##################################    Update serialzer  worked !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return instance
    

class UserDetailsSeriallzer(ModelSerializer):
    class Meta:
        model = UserBasicDetails
        fields = "__all__"
    
    def update(self, instance, validated_data, user):
        
        try:
            user_birthday = UserProfile.objects.filter(user = user)
        except:
            print("value not found")
        instance.mother_tongue = validated_data.get('mother_tongue', instance.mother_tongue)
        instance.eating_habit = validated_data.get('eating_habit', instance.eating_habit)
        instance.drinking_habit = validated_data.get('drinking_habit', instance.drinking_habit)
        instance.smoking_habit = validated_data.get('smoking_habit', instance.smoking_habit)
        instance.martial_status = validated_data.get('martial_status', instance.martial_status)
        instance.height = validated_data.get('height', instance.height)
        instance.body_type = validated_data.get('body_type', instance.body_type)
        instance.physical_status = validated_data.get('physical_status', instance.physical_status)
                                                    
