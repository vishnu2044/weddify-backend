from django.urls import path

from . import views

urlpatterns = [
    path('getmatcheslocationbased/', views.get_matches_location_based, name='get_matches_location_based'),
    path('getallmatches/', views.get_all_matches, name='get_all_matches'),
    path('getmatchprofile/<int:match_id>/', views.get_match_profile, name='get_match_profile'),
    path('newmatches/', views.new_matches, name='new_matches'),

]