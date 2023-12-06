from rest_framework import serializers
from user_accounts.models import PremiumVersion

class PremiumUserSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateTimeField(format="%Y-%m-%d")
    
    class Meta:
        model = PremiumVersion
        fields = ('plan_name', 'amount_paid', 'expiry_date', 'plan_count')
    