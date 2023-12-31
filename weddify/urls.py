"""
URL configuration for weddify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user_accounts import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('userauth/', include('user_accounts.urls')),
    path('signup/', views.Register.as_view(), name='signup'),
    path('userprofile/', include('user_profile.urls')),
    path('userpreferences/', include('user_preferences.urls')),
    path('preferedmatches/', include('preferred_matches.urls')),
    path('adminpanel/', include('admin_panel.urls')),
    path('chat_app/', include('chat_app.urls')),
    path('create-checkout-session/', include('stripe_payment.urls')),

    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
