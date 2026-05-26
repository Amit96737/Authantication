from django.db import models
from users.models.users import User
from common.models.common import CommonFields

class FCMToken(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.TextField(blank=True
                             )
    device_type = models.CharField(max_length=100, null=True, blank=True)
    os = models.CharField(max_length=200, null=True, blank=True)
    browser = models.CharField(max_length=200, null=True, blank=True)