from django.conf import settings
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import status
from user_accounts.models import UserProfile, PremiumVersion
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from datetime import datetime, timedelta



stripe.api_key = settings.STRIPE_SECRET_KEY


YOUR_DOMAIN = 'http://localhost:4242'


class StripeCheckOutView(APIView):
    def post(self, request):
        data = request.data
        amount = data['total_amount']
        caption = data['premium_type']
        user_id = data ['user_id']
        plan_type = data['type']
        duration = data['duration']

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(data)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")



        try:
            print('asdfgh')
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
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '/?canceled=true'
            )
                
            return Response(checkout_session.url, status=status.HTTP_200_OK)
                
        except:
            return Response(
                {'error':'something went wrong when creating stripe checkout session'},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def setup_User_premium_details(request, data):
    user = request.user
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print('data', data)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    try:
        user_profile = UserProfile.objects.get(user = user)
        return user_profile
    except UserProfile.DoesNotExist:
        return Response({"error" : 'user profile is not created yet '}, status=status.HTTP_400_BAD_REQUEST)





            # if checkout_session:
            #     try:
            #         user = User.objects.get(id = user_id)
            #         try:
            #             user_profile = UserProfile.objects.get(user = user)
            #             user_profile.is_premium_user = True
            #             user_profile.save() 

            #             if plan_type == 'month':
            #                 days = duration * 30
            #             else:
            #                 days = duration * 365
            #             current_date = datetime.now()
            #             print(current_date,"current date >>>>>>>>>>>>>")
            #             print(timedelta(days = days),"total days >>>>>>>>>>>>>")

            #             expairy_date = current_date + timedelta(days = days)
            #             try:
            #                 premium = PremiumVersion.objects.get(user=user)
            #             except PremiumVersion.DoesNotExist:
            #                 premium = PremiumVersion.objects.create(
            #                     user=user, 
            #                     expairy_date=expairy_date, 
            #                     plan_name=plan_type,
            #                     amount_paid = amount
            #                     )
            #         except UserProfile.DoesNotExist:
            #             return Response({"error" : 'user profile is not created yet'}, status=status.HTTP_400_BAD_REQUEST)

            #     except User.DoesNotExist:
            #         return Response({"error" : 'user is not valid'}, status=status.HTTP_401_UNAUTHORIZED)