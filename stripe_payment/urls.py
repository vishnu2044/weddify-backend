from django.urls import path
from .views import StripeCheckOutView, update_premium_status

urlpatterns = [
    path('strip-checkout/', StripeCheckOutView.as_view()),
    path('update-premium-status/', update_premium_status),
    
]
