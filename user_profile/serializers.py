from django.contrib.auth.models import User
from rest_framework import serializers
from user_accounts.models import UserProfile
from rest_framework.serializers import ImageField, ValidationError, ModelSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import UserBasicDetails, ProfessionalDetails, ReligionalDetails



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
        instance.unique_user_id = self.context.get("user_unique_id")
        instance.save()


        print("##################################    Update serialzer  worked !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return instance
    



class UserDetailsSeriallzer(serializers.ModelSerializer):
    class Meta:
        model = UserBasicDetails
        fields = ('mother_tongue', 'eating_habit', 'drinking_habit', 'smoking_habit', 'martial_status', 'height', 'body_type', 'physical_status', 'location', 'citizenship' )

    def update(self, instance, validated_data):
        # Update the instance with validated_data
        print("::::::::::::::::::::::::::: serializer updating is working::::::::::::::::::::::::::::::::")
        instance.mother_tongue = validated_data.get('mother_tongue', instance.mother_tongue)
        instance.age = self.context.get("user_age")
        instance.eating_habit = validated_data.get('eating_habit', instance.eating_habit)
        instance.drinking_habit = validated_data.get('drinking_habit', instance.drinking_habit)
        instance.smoking_habit = validated_data.get('smoking_habit', instance.smoking_habit)
        instance.martial_status = validated_data.get('martial_status', instance.martial_status)
        instance.height = validated_data.get('height', instance.height)
        instance.body_type = validated_data.get('body_type', instance.body_type)
        instance.physical_status = validated_data.get('physical_status', instance.physical_status)
        instance.location = validated_data.get('location', instance.location)
        instance.citizenship = validated_data.get('citizenship', instance.citizenship)

        # Save the instance after updating
        instance.save()
        return instance
    
class UserProfessionalDetailsSeriallzer(ModelSerializer):
    print("creating of profession works::::::::::::::::::::::::::::::::::::::::::::::::")
    class Meta:
        model = ProfessionalDetails
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.education = validated_data.get('education', instance.education)
        instance.college = validated_data.get('college', instance.college)
        instance.working_sector = validated_data.get('working_sector', instance.working_sector)
        instance.income = validated_data.get('income', instance.income)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()

        return instance
    
class UserReligionalDetailsSeriallzer(ModelSerializer):
    print("creating of religious details works::::::::::::::::::::::::::::::::::::::::::::::::")
    class Meta:
        model = ReligionalDetails
        fields = "__all__"

    def update(self, instance, validated_data):
        instance.religion = validated_data.get('religion', instance.religion)
        instance.caste = validated_data.get('caste', instance.caste)
        instance.star = validated_data.get('star', instance.star)

        instance.save()

        return instance
