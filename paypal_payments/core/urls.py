from django.urls import path
from . import views

urlpatterns = [
    path('paypal-about-page/', views.paypal_about_page, name='paypal_about_page'),
    path('plan-page/', views.plan_page, name='plan_page'),
    path('initiate-payment/<uuid:plan_id>/', views.initiate_paypal_payment, name='initiate_paypal_payment'),
    path('paypal-payment-success/', views.payment_success_view, name='payment_success'),
    path('paypal-payment-cancelled/', views.payment_cancelled_view, name='payment_cancelled'),
]