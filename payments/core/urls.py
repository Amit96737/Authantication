from django.urls import path
from . import views

urlpatterns = [
    path("about/", views.stripe_about_page, name="stripe_about_page"),
    path("item-details/", views.item_detail, name="item_detail"),
    path("create-checkout-session/<uuid:id>/", views.create_checkout_session, name="create_checkout_session"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("success/", views.success, name="success"),
    path("cancel/", views.cancel, name="cancel"),
    path("favourite-items/<uuid:id>/", views.favourite_items, name="favourite_items"),
    path("item/<uuid:id>/", views.specific_item_detail, name="specific_item_detail"),
    path('add-to-cart/<uuid:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('delete-cart-item/<uuid:id>/', views.delete_cart_item, name='delete_cart_item'),
]