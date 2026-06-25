from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sign-up/", views.user_sign_up, name="user_sign_up"),
    path("verify-email-otp/", views.verify_email_otp, name="verify_email_otp"),
    path("verify-sms-otp/", views.verify_sms_otp, name="verify_sms_otp"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),

    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path('verify-forgot-otp/', views.verify_forgot_otp, name='verify_forgot_otp'),
    path("set-new-password/", views.set_new_password, name="set_new_password"),
]

