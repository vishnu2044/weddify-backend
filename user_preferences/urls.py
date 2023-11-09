from django.urls import path

from . import views

urlpatterns = [
    path('getbasicpreferences/', views.get_basic_preferences, name='get_basic_preferences'),
    path('updatebasicpreferences/', views.update_basic_preferences, name='update_basic_preferences'),

    path('getprofessionalpreferences/', views.get_professional_preferences, name='get_professional_preferences'),
    path('updateprfessionalpreference/', views.update_prfessional_preference, name='update_prfessional_preference'),

    path('getreligiouspreferences/', views.get_religious_preferences, name='get_religious_preferences'),
    path('updatereligiounalpreference/', views.update_religiounal_preference, name='update_religiounal_preference'),
    
]