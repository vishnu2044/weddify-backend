from django.urls import path

from . import views

urlpatterns = [
    path('getmatcheslocationbased/', views.get_matches_location_based, name='get_matches_location_based'),
    path('getallmatches/', views.get_all_matches, name='get_all_matches'),
    path('getmatchprofile/<int:match_id>/', views.get_match_profile, name='get_match_profile'),
    path('newmatches/', views.new_matches, name='new_matches'),
    path('viewed_profiles/', views.viewed_profiles, name='viewed_profiles'),
    path('matchesviewedyours/', views.matches_viewed_yours, name='matches_viewed_yours'),
    path('like_match/<int:match_id>/', views.like_match, name='like_match'),
    path('blockuser/<int:block_user>/', views.block_user, name='block_user'),
    path('unlike_match/<int:match_id>/', views.unlike_match, name='unlike_match'),
    path('check_profile_completed/', views.check_profile_completed, name='check_profile_completed'),
    path('get_filter_details/', views.get_filter_details, name='get_filter_details'),
    path('filtering_matches/', views.filtering_matches, name='filtering_matches'),
    path('search_matches/', views.search_matches, name='search_matches'),
    path('liked_you_matches/', views.liked_you_matches, name='liked_you_matches'),

]