from django.conf import settings
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from user_accounts.models import UserProfile, PremiumVersion
from .serializer import PremiumUserSerializer

from django.contrib.auth.models import User
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils import timezone



stripe.api_key = settings.STRIPE_SECRET_KEY


# YOUR_DOMAIN = 'http://localhost:4242'
YOUR_DOMAIN = 'http://localhost:3000'


class StripeCheckOutView(APIView):
    def post(self, request):
        data = request.data
        amount = data['total_amount']
        caption = data['premium_type']
        user_id = data ['user_id']  
        plan_type = data['type']
        duration = data['duration'] 
        try:
            checkout_session = stripe.checkout.Session.create(
                 line_items=[{
                    'price_data': {
                        'currency': 'INR',
                        'product_data': {
                            'name': 'Premium purchase ' + caption,
                            # 'images': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fdepositphotos.com%2Fphotos%2Fpremium.html&psig=AOvVaw3a-8Go47VUPiwSPTDQRf4_&ust=1701261623005000&source=images&cd=vfe&ved=0CBIQjRxqFwoTCNi5yMfb5oIDFQAAAAAdAAAAABAE'
                        },
                        'unit_amount': amount * 100
                    },
                    'quantity': 1
                }],
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.SITE_URL + f'/?success=true&amount={amount}&plan_type={plan_type}&duration={duration}&user_id={user_id}',
                cancel_url=settings.SITE_URL + '/?canceled=true'
            )

                
            return Response(checkout_session.url, status=status.HTTP_200_OK)
                
        except:
            return Response(
                {'error':'something went wrong when creating stripe checkout session'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['POST'])
def update_premium_status(request):
    user_id = request.POST.get("user_id")
    total_amount = request.POST.get("totalAmount")
    plan_type = request.POST.get("planType")
    duration = request.POST.get("duration")

    user = User.objects.get(id=user_id)

    try:
        with transaction.atomic():
            user_profile = UserProfile.objects.get(user=user)
            user_profile.is_premium_user = True
            user_profile.save()
            current_time = timezone.now()
            if plan_type == 'month':
                expairy_date = current_time + relativedelta(months=int(duration))
            else:
                expairy_date = current_time + relativedelta(years=int(duration))
            try:
                premium = PremiumVersion.objects.get(user=user)
                premium.amount_paid = int(total_amount)
                premium.save()
            except PremiumVersion.DoesNotExist:
                PremiumVersion.objects.create(
                    user=user,
                    expiry_date=expairy_date,
                    plan_name=plan_type,
                    plan_count = duration,
                    amount_paid=int(total_amount)
                )
            return Response({'message': 'success'}, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response({"error": 'user profile is not created yet'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_is_premium(request):
    user = request.user
    try:
        premium_user = UserProfile.objects.get(user = user, is_premium_user = True)
        try:
            plan_details = PremiumVersion.objects.get(user = user)
            serializer = PremiumUserSerializer(plan_details)
            return Response(data = serializer.data, status= status.HTTP_200_OK)
        except PremiumVersion.DoesNotExist:
            return Response({"message" : "user dont have premium"}, status=status.HTTP_404_NOT_FOUND)

    except UserProfile.DoesNotExist:
        return Response({"message" : "user dont have premium"}, status=status.HTTP_404_NOT_FOUND)

