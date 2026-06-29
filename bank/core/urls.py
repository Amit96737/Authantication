from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.bank_dashboard, name="bank_dashboard"),
    path("create-account/", views.create_account, name="create_account"),
]

