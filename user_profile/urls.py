from django.urls import path

from . import views

urlpatterns = [
    path('userdetails/' , views.get_user_profile, name='userdatails'),
    path('updateprofile/', views.UpdateUserProfile, name='updateprofile' ),

    path('userprofile/', views.get_basic_details, name='getbasicdetails'),
    path('updatebasicdetails/', views.update_basic_details, name='update_basic_details'),

    path("getprofessionaldetails/", views.get_professional_details, name='get_professional_details' )
]
