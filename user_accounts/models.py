from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    data = models.TextField()

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    unique_user_id = models.CharField(max_length=100, blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_images',blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank = True, null = True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField( max_length=50, blank=True, null=True)
    is_premium_user = models.BooleanField(default=False)

class PremiumVersion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan_name = models.CharField(max_length=150, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    
