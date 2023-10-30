from rest_framework.serializers import ModelSerializer, ValidationError
from user_accounts.models import Note, UserProfile
from django.contrib.auth.models import User


class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class UserRegister(ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'password', 'email', 'id']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username is already taken.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('This email is already taken !')
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        profile = UserProfile.objects.create(user=instance)
        return instance



class UserProfileRegistrationSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    
    


