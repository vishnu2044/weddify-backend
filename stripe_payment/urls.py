from django.urls import path
from .views import StripeCheckOutView, update_premium_status, check_user_is_premium

urlpatterns = [
    path('strip-checkout/', StripeCheckOutView.as_view()),
    path('update-premium-status/', update_premium_status),
    path('check-user-is-premium/', check_user_is_premium),
    
]
