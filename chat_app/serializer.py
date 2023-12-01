from rest_framework.serializers import ModelSerializer, ValidationError
from .models import ChatMessage
from django.contrib.auth.models import User
from user_accounts.models import UserProfile
from rest_framework import serializers



class ProfileSerializer(ModelSerializer):
    profile_img = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_img')

    def get_profile_img(self, obj):
        try:
            data = UserProfile.objects.get(user=obj)
            if data.profile_img :
                return data.profile_img.url
            else:
                return None
        except UserProfile.DoesNotExist:
            return None


class MessageSerializer(ModelSerializer):
    reciever_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'reciever_profile', 'sender_profile', 'reciever', 'message', 'is_read', 'date' ]



class ChatListSerializer(serializers.ModelSerializer):

    profile_img = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['username', 'profile_img', 'id', 'unread']
    
    def get_profile_img(self, obj):
        try:
            data = UserProfile.objects.get(user__username = obj)
            if data.profile_img: 
                return data.profile_img.url
            else:
                return None
        except UserProfile.DoesNotExist:
            return None
        
    def get_username(self, obj):
        try:
            user = User.objects.get(username=obj)
            if user.username:
                return user.username
            else:
                return None
        except User.DoesNotExist:
            return None
        
        
    def get_id(self, obj):
        try:
            user = User.objects.get(username=obj)
            return user.id
        except User.DoesNotExist:
            return None
        
        
    def get_unread(self, obj):
        user_id = self.context.get('user_id')
        user = User.objects.get(pk=user_id)
        username = user.username
        unread_count = ChatMessage.objects.filter(reciever__username=obj, sender__username=username, is_read=False).count()
        print(unread_count)
        print(user,"  reciever >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(obj,"sender  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")     
        return unread_count
        

