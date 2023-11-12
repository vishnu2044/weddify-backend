from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timezone, datetime


# Create your models here.
class UserBasicDetails(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE, null = True )
    age = models.IntegerField( blank =True, null =True, validators=[MinValueValidator(18)] )
    mother_tongue = models.CharField( max_length=100, blank=True, null=True )
    eating_habit = models.CharField( max_length=100, blank=True, null=True )
    drinking_habit = models.CharField( max_length=100, blank=True, null=True )
    smoking_habit = models.CharField( max_length=100, blank=True, null=True )
    profile_created_for = models.CharField( max_length=100, blank=True, null=True )
    martial_status = models.CharField( max_length=100, blank=True, null=True )
    height = models.DecimalField( max_digits=5, decimal_places=2, blank=True, null=True)
    body_type = models.CharField( max_length=100, blank=True, null=True )
    physical_status = models.CharField( max_length=100, blank=True, null=True )
    location = models.CharField( max_length=100, blank=True, null=True )
    citizenship = models.CharField( max_length=100, blank=True, null=True )
    
    


class ProfessionalDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    education = models.CharField( max_length=255, null=True, blank=True)
    college = models.CharField( max_length=255, null=True, blank=True)
    working_sector = models.CharField( max_length=255, null=True, blank=True)
    income = models.CharField( max_length=255, null=True, blank=True)
    occupation = models.CharField( max_length=255, null=True, blank=True)
    organization = models.CharField( max_length=255, null=True, blank=True)
    working_location = models.CharField( max_length=255, null=True, blank=True)
    


class ReligionalDetails(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE, null=True)
    religion = models.CharField(max_length=100)
    caste = models.CharField( max_length=100)
    star = models.CharField( max_length=100)


class UserBlockedList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocking_user', null=True)
    blocked_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_user')
    blocked_time = models.DateTimeField(auto_now_add=True)


class ProfileVisitedUsers(models.Model):
    user = models.ForeignKey(User, related_name='visited_user', on_delete=models.CASCADE, null=True)
    visited_profile = models.ForeignKey(User, related_name='visited_profile', on_delete=models.CASCADE, null=True)
    visited_time = models.DateTimeField(auto_now_add=True)


class ProfileLikeList(models.Model):
    user = models.ForeignKey(User, related_name='liked_user', on_delete=models.CASCADE, null=True)
    liked_profile = models.ForeignKey(User, related_name='liked_profile', on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now=True)


class Country(models.Model):
    country_name = models.CharField( max_length=150)

class Cities(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=150) 

