from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import (TokenRefreshView,)
# , YourModelView

app_name = "account_api"
urlpatterns = [
    path('sign-up/', UserRegistrationAPIView.as_view(), name='sign_up'),
    path('log-in/', UserLoginView.as_view(), name='log_in'),
    path('verify/', UserVerificationAPIView.as_view(), name='verify'),
    path('log-in/refresh/', TokenRefreshView.as_view(), name='log_in_refresh'),
    path('log-out/', UserLogoutView.as_view(), name='log_out'),
    path('forget-pass/', ForgetPassAPIView.as_view(), name='forget_pass'),
    path('reset-pass/', ResetPassAPIView.as_view(), name='reset_pass'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('resend-verificaiton-code/', ResendVerificationCode.as_view(), name='resend_verification_code')
    # path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    # path('email/verify/<str:token>', VerifyEmailApiView.as_view(), name='email_verify'),
    # path('email/resend/', ResendEmailVerificationApiView.as_view(), name='resend_email'),
    # path('email/reset-password/', ResetPasswordEmail.as_view(), name='send_reset_password_email'),
    # path('reset-password/<str:token>', ResetPasswordConfirm.as_view(), name='reset_password'),
    
    # # this part is ralet to profile

    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('adress/', AdressApiView.as_view(), name='address'),
    # path('yourmodel/', YourModelView.as_view() )
]