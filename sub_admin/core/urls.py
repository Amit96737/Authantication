from django.urls import path
from . import views
from . import services

urlpatterns = [
    path('user-verify/', views.users_verification, name="users_verification"),
    path('approve-user/<str:id>/', views.approve_user, name='approve_user'),
    path('reject-user/<str:id>/', views.reject_user, name='reject_user'),

    path('dashboard/', views.sub_admin_dashboard, name="sub_admin_dashboard"),

    # User Management Section
    path('user-management/', views.user_management, name="user_management"),
    path('user-details/<str:id>/', views.user_detail, name="user_detail"),
    path('download-csv/', services.download_users_csv, name='download_csv'),
    # path('user-update/<str:id>/', views.update_user, name="update_user"),

    # Crud Management Section
    path('crud-management/', views.crud_management, name="crud_management"),
    # path('student-details/<str:id>/', views.student_detail, name="student_detail"),

    # Crud Management Section
    path('bank-management/', views.bank_management, name="bank_management"),
    path('identity-verification/', views.identity_verification, name="identity_verification"),
    path('approve-verification/<str:id>/', views.approve_verification, name='approve_verification'),
    path('reject-verification/<str:id>/', views.reject_verification, name='reject_verification'),

    # Crud Management Section
    path('stripe-management/', views.stripe_management, name="stripe_management"),
    path('download-item-csv/', services.download_items_csv, name='download_items_csv'),

    path('paypal-management/', views.paypal_management, name="paypal_management"),

    # Sub-Admin Section
    path('sub-admin-user/', views.sub_admin_user, name='sub_admin_user'),
    path('toggle-sub-admin/<str:id>/', views.toggle_sub_admin, name='toggle_sub_admin'),

    path('settings/', views.sub_admin_settings, name="sub_admin_settings"),
]