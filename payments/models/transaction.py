from django.db import models
from payments.models.product import Item
from users.models.users import User
from common.models.common import CommonFields

class Transaction(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=20)
    status = models.CharField(max_length=50)

    payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    webhook_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.item} - {self.status}"