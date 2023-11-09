from django.contrib.auth.models import User
from rest_framework import serializers
from . import models

class BasicPreferencesSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.BasicPreferences
        fields = '__all__'


    def update(self, instance, validated_data):
        # Update the instance with validated_data
        print("::::::::::::::::::::::::::: serializer updating is working::::::::::::::::::::::::::::::::")
        instance.mother_tongue = validated_data.get('mother_tongue', instance.mother_tongue)
        instance.age_from = validated_data.get('age_from', instance.age_from)
        instance.age_to = validated_data.get('age_to', instance.age_to)
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
    

class ProfessionalPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProfessionalPreferences
        fields = "__all__"
    
    def update(self, instance, validated_data):
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! professional preference serializer is working!!!!!!!!!!!!!!")
        instance.education = validated_data.get('education', instance.education)
        instance.college = validated_data.get('college', instance.college)
        instance.working_sector = validated_data.get('working_sector', instance.working_sector)
        instance.income = validated_data.get('income', instance.income)
        instance.occupation = validated_data.get('occupation', instance.occupation)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.save()
        print("instance saved !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        return instance
    

class ReligiounalPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReligionalPreferences
        fields  = '__all__'

    def update(self, instance, validated_data):
        instance.religion = validated_data.get('religion', instance.religion)
        instance.caste = validated_data.get('caste', instance.caste)
        instance.star = validated_data.get('star', instance.star)
        instance.save()
        return instance

