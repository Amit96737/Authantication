from rest_framework import serializers
from notification.models.fcm import FCMToken
from users.serializers.custom import CustomSerializer

class FcmTokenSerializer(CustomSerializer, serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ['id', 'token', 'device_type', 'os', 'browser']