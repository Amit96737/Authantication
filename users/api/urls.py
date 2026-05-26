from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,)

urlpatterns = [
    # get token
    path('token/access/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user api
    path('sign-up/', views.SignUpAPIView.as_view(), name='sign_up'),
    path('verify-email-otp/', views.VerifyEmailOtpAPIView.as_view(), name='verify_email_otp'),
    path('verify-sms-otp/', views.VerifySMSOtpAPIView.as_view(), name='verify_sms_otp'),
    path('sign-in/', views.SignInAPIView.as_view(), name='sign_in'),
    path('sign-out/', views.SignOUTAPIView.as_view(), name='sign_out'),
    path('user-profile/', views.UserProfileAPIView.as_view(), name='user_profile'),
    path('change-password/', views.UserChangePasswordAPIView.as_view(), name='change_password'),
    path('forgot-password-mail/', views.UserRequestForgotPasswordAPIView.as_view(), name='forgot_password_mail'),
    path('verify-forgot-password/', views.ValidateForgetPasswordOtpAPIView.as_view(), name='verify_forgot_password'),
    path('reset-password/', views.ResetPasswordAPIView.as_view(), name='reset_password'),
    path('delete-account/', views.DeleteAccountAPIView.as_view(), name='delete_account'),
]