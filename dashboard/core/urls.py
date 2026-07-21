from django.urls import path
from . import views

urlpatterns = [
    path('subscription/', views.plan_page_onboard, name='plan_page_onboard'),
    path('activate-free-plan/', views.activate_free_plan, name='activate_free_plan'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("sign-up", views.user_sign_up, name="user_sign_up"),
    path("verify-email-otp/", views.verify_email_otp, name="verify_email_otp"),
    path("verify-sms-otp/", views.verify_sms_otp, name="verify_sms_otp"),

    path("resend-email-otp/", views.resend_email_otp, name="resend_email_otp"),
    path("resend-sms-otp/", views.resend_sms_otp, name="resend_sms_otp"),

    path("", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path('verify-forgot-otp/', views.verify_forgot_otp, name='verify_forgot_otp'),
    path("set-new-password/", views.set_new_password, name="set_new_password"),
    path("user-profile/", views.user_profile, name="user_profile"),
    path("update-profile", views.update_profile, name="update_profile"),
    path("delete-profile", views.delete_profile, name="delete_profile"),
]
