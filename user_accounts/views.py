from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.serializers import  ValidationError

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from.serializers import NoteSerializer, UserRegister
from .models import Note


# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class Register(APIView):
    
    def post(self, request, format=None):
        serializer = UserRegister(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'registered'
            data['username'] = account.username
            data['email'] = account.email
        else:
            data = serializer.errors
        return Response(data , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getRouts(request):
    routes = [
        'api/token',
        '/api/token/refresh'
    ]
    return Response(routes)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    user =  request.user
    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)



