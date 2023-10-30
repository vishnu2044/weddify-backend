from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


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
