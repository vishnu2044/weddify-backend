from django.urls import path

from .views import get_user_profile, UpdateUserProfile, get_basic_details

urlpatterns = [
    path('userdetails/' , get_user_profile, name='userdatails'),
    path('updateprofile/', UpdateUserProfile, name='updateprofile' ),
    path('userprofile/', get_basic_details, name='getbasicdetails'),
]
