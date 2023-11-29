from django.urls import path
from .views import StripeCheckOutView

urlpatterns = [
    path('strip-checkout/', StripeCheckOutView.as_view())
]
