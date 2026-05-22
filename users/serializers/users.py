from rest_framework import serializers
from users.serializers.custom import CustomSerializer
from users.models import User


class UserSerializer(CustomSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'profile_pic', 'gender', 'biograph', 'phone_number',
                  'email_verified', 'sms_verified']


class ChangePasswordSerializer(CustomSerializer, serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError('new_password and confirm_password does not match')

        return attrs


class ForgotPasswordsSerializer(CustomSerializer, serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = User.objects.filter(email=email)
        if user.exists() is False:
            raise serializers.ValidationError('We could not  find an account associated with this email.')
        attrs['user'] = user.first()

        return attrs

class ForgotOtpVerificationSerializer(CustomSerializer, serializers.Serializer):
    email = serializers.EmailField()

    otp = serializers.IntegerField(min_value=100000, max_value=999999,
                                   error_messages={
                                       'min_value': 'OTP must be a 6-digit number.',
                                       'max_value': 'OTP must be a 6-digit number.',
                                       'invalid': 'Invalid OTP. Please enter a valid 6-digit number.'
                                   })

    def validate(self, attrs):
        email = attrs.get("email").lower()
        user = User.objects.filter(email=email)
        if user.exists() is True:
            attrs['user'] = user.first()
        else:
            raise serializers.ValidationError({"email": "email does not exists"})

        return attrs
