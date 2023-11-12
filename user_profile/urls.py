from django.urls import path

from . import views

urlpatterns = [
    path('userdetails/' , views.get_user_profile, name='userdatails'),
    path('updateprofile/', views.UpdateUserProfile, name='updateprofile' ),

    path('getbasicdetails/', views.get_basic_details, name='getbasicdetails'),
    path('updatebasicdetails/', views.update_basic_details, name='update_basic_details'),

    path("getprofessionaldetails/", views.get_professional_details, name='get_professional_details' ),
    path("updateprofessionaldata/", views.update_professional_data, name='update_professional_data' ),

    path("getreligionaldetails/", views.get_religional_details, name='get_religional_details' ),
    path("updatereligionaldata/", views.update_religional_data, name='update_religional_data' ),

    path('get_blocked_matches/', views.get_blocked_matches, name='get_blocked_matches'),
    path('unblock_match/<int:match_id>/', views.unblock_match, name='unblock_match'),
]
