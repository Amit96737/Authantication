from django.db import models
from common.models.common import CommonFields

class BlockUser(CommonFields):
    blocker = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="blocking")
    blocked = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="blocked")

    class Meta:
        unique_together = ("blocker", "blocked")
