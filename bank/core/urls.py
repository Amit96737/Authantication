from django.urls import path
from . import views

urlpatterns = [
    path("bank-about-page/", views.bank_about_page, name="bank_about_page"),
    path("home/", views.bank_dashboard, name="bank_dashboard"),
    path("create-account/", views.create_account, name="create_account"),
    path('activate/<uuid:id>/', views.activate_account, name='activate_account'),
    path('deactivate/<uuid:id>/', views.deactivate_account, name='deactivate_account'),
    path("all-records/", views.all_records, name="all_records"),
    path("create-bank/", views.create_bank, name="create_bank"),
    path("all-banks/", views.all_banks, name="all_banks"),
]

