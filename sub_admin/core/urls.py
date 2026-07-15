from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.sub_admin_dashboard, name="sub_admin_dashboard"),

    # User Management Section
    path('user-management/', views.user_management, name="user_management"),
    path('user-details/<str:id>/', views.user_detail, name="user_detail"),
    # path('user-update/<str:id>/', views.update_user, name="update_user"),

    # Crud Management Section
    path('crud-management/', views.crud_management, name="crud_management"),
    # path('student-details/<str:id>/', views.student_detail, name="student_detail"),

    # Crud Management Section
    path('bank-management/', views.bank_management, name="bank_management"),

    # Crud Management Section
    path('stripe-management/', views.stripe_management, name="stripe_management"),

    path('paypal-management/', views.paypal_management, name="paypal_management"),
    path('settings/', views.sub_admin_settings, name="sub_admin_settings"),
]