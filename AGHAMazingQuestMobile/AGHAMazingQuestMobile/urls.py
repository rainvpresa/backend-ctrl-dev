"""
URL configuration for AGHAMazingQuestMobile project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from accounts.social import GoogleLogin
from accounts.views import (
    ProfileView,
    OTPRequestView,
    OTPVerifyView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)
from .views import APIRootView


urlpatterns = [
    path('admin/', admin.site.urls),
    # API root for quick discovery
    path('api/', APIRootView.as_view(), name='api_root'),
    # dj-rest-auth endpoints (login/logout/password reset/token refresh)
    path('api/auth/', include('dj_rest_auth.urls')),
    # registration (optional) and social auth
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    # Google token-exchange endpoint for mobile apps
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    # profile and OTP endpoints
    path('api/auth/profile/', ProfileView.as_view(), name='api_profile'),
    path('api/auth/otp/request/', OTPRequestView.as_view(), name='otp_request'),
    path('api/auth/otp/verify/', OTPVerifyView.as_view(), name='otp_verify'),
    # password reset (forgot password) endpoints
    path('api/auth/password/reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/', include('allauth.urls')),
    
]
