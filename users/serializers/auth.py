from rest_framework import serializers
from users.models.users import User
from users.serializers.custom import CustomSerializer
from notification.serializers.fcm_serializers import FcmTokenSerializer

class UserSignInSerializer(CustomSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    fcm = FcmTokenSerializer(required=False)


    def validate(self, data):
        email = data.get("email").lower()
        password = data.get("password")

        user = User.objects.filter(email=email).first()

        if not user:
            raise serializers.ValidationError("User not found with this email address")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password please try again")

        if not user.email_verified:
            raise serializers.ValidationError("Email not verified please verify your email address")

        if not user.sms_verified:
            raise serializers.ValidationError("SMS not verified please verify sms address")

        data['user'] = user
        return data


class SocialAuthSerializer(CustomSerializer, serializers.Serializer):
    token = serializers.CharField()
    PLATFORM_CHOICE = [
        ('Google', 'Google'),
        ('Apple', 'Apple'),
    ]
    platform = serializers.ChoiceField(choices=PLATFORM_CHOICE)
    fcm = FcmTokenSerializer(required=False)


