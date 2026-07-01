from django.db import models
from common.models.common import CommonFields
from bank.models.account import BankAccount

class Transaction(CommonFields):
    TRANSACTION_TYPE = (
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdraw"),
        ("TRANSFER", "Transfer"),
    )
    sender = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="sent_transactions", null=True, blank=True)
    receiver = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="received_transactions", null=True, blank=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_type}"