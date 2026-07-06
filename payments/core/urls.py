from django.urls import path
from . import views

urlpatterns = [
    path("item-details/", views.item_detail, name="item_detail"),
    path("create-checkout-session/<uuid:id>/", views.create_checkout_session, name="create_checkout_session"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
]