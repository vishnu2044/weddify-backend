from django.urls import path

from . import views

urlpatterns = [
    path('getmatcheslocationbased/', views.get_matches_location_based, name='get_matches_location_based'),
    path('getallmatches/', views.get_all_matches, name='get_all_matches'),
    path('getmatchprofile/<int:match_id>/', views.get_match_profile, name='get_match_profile'),
    path('newmatches/', views.new_matches, name='new_matches'),
    path('blockuser/<int:block_user>/', views.block_user, name='block_user'),
    path('viewed_profiles/', views.viewed_profiles, name='viewed_profiles'),
    path('matchesviewedyours/', views.matches_viewed_yours, name='matches_viewed_yours'),
    path('like_match/<int:match_id>/', views.like_match, name='like_match'),
    path('unlike_match/<int:match_id>/', views.unlike_match, name='unlike_match'),
    path('check_profile_completed/', views.check_profile_completed, name='check_profile_completed'),

]