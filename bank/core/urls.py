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

    path("deposit-bank/", views.deposit, name="deposit_amount"),
    path("withdraw-bank/", views.withdraw, name="withdraw_amount"),
    path("check-balance/", views.check_balance, name="check_balance"),
    path("specific-account/", views.specific_account, name="specific_account"),
    path("transfer-amount/", views.transfer_amount, name="transfer_amount"),
    path("transaction-history/", views.transaction_history, name="transaction_history"),

    path("identity-verification/", views.identity_verification, name="identity_verification"),
]

