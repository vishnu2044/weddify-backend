from django.db import models

# Create your models here.

class PremiumPlans(models.Model):
    monthly_price = models.IntegerField( null=True, blank=True)
    yearly_price = models.IntegerField( null=True, blank=True)
    updated_time  = models.DateField(auto_now=True)