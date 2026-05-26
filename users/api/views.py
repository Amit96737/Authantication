from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from users.serializers.user_signup import UserSignUpSerializer, OtpVerificationSerializer, SMSOTPVerificationSerializer
from rest_framework import status
from users.serializers.users import UserSerializer, ChangePasswordSerializer, ForgotPasswordsSerializer, ForgotOtpVerificationSerializer, ResetPasswordSerializer
from users.helper.response import success_response, error_response, response_not_found, create_unique_username
from users.services.send_otp_verification import send_otp_to_mail, send_otp_to_phone, send_forget_password_otp
from users.models import User
from django.core.cache import cache
from users.serializers.auth import UserSignInSerializer
from notification.models.fcm import FCMToken
from users.serializers.follow_serializers import UserFollowSerializer
from users.models.follow import Follow


class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            email = email.lower()
        user_exists = User.objects.filter(email=email).first()
        if user_exists and not user_exists.email_verified:
            send_otp_to_mail(username=f'{user_exists.first_name} {user_exists.last_name}', user_email=user_exists.email.lower())
            return success_response(
                message="OTP sent to your email. Please verify your account.",
                status_code=status.HTTP_200_OK
            )

        if user_exists and user_exists.email_verified:
            return error_response(message="An account is already registered with this email address. Please proceed to login.",
                                    status_code=status.HTTP_400_BAD_REQUEST)

        serializer = UserSignUpSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(username=create_unique_username(serializer.validated_data['first_name'],
                                                                   serializer.validated_data['last_name']))
            user.set_password(serializer.validated_data['password'])
            user.is_active = True
            user.save()

            send_otp_to_mail(username=f'{user.first_name} {user.last_name}', user_email=user.email.lower())

            serialize = UserSerializer(user)
            return success_response(message="User registered successfully please verify your account", data=serialize.data, status_code=status.HTTP_201_CREATED)


class VerifyEmailOtpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            if user.email_verified is True:
                return error_response(
                    message="your email is already verified.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            cache_otp = cache.get(f"otp_{user.email}")

            if cache_otp is None:
                send_otp_to_mail(username=f'{user.first_name} {user.last_name}', user_email=user.email.lower()
                                 )
                return response_not_found(
                    message="your previous opt was expired. we have resend otp please check your mail.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if str(cache_otp) == str(serializer.validated_data['otp']):
                user.email_verified = True
                user.save()
                send_otp_to_phone(
                    username=f'{user.first_name} {user.last_name}',
                    phone_number=user.phone_number
                )
                return success_response(message="email verified & SMS otp sent successfully", status_code=status.HTTP_200_OK
                                        )
            else:
                return error_response(
                    message="Invalid otp code",
                    status_code=status.HTTP_400_BAD_REQUEST)


class VerifySMSOtpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SMSOTPVerificationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            if user.sms_verified is True:
                return error_response(
                    message="your sms otp is already verified. please login.",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            cache_otp = cache.get(f"sms_otp_{user.phone_number}")

            if cache_otp is None:
                send_otp_to_phone(
                    username=f'{user.first_name} {user.last_name}',
                    phone_number=user.phone_number
                )
                return error_response(
                    message="your previous otp was expired. we have resend otp please check your phone.",
                    status_code=status.HTTP_400_BAD_REQUEST)

            if str(cache_otp) == str(serializer.validated_data['otp']):
                user.sms_verified = True
                user.save()

                return success_response(
                    message="sms otp verified successfully please login.",
                    status_code=status.HTTP_200_OK
                )

            return error_response(
                message="Invalid otp code",
                status_code=status.HTTP_400_BAD_REQUEST
            )


class SignInAPIView(APIView):
    permission_classes = [AllowAny]

    def handle_fcm_token_generate(self, user, fcm_data):

        # FCMToken.objects.filter(user=user).delete()

        FCMToken.objects.update_or_create(
            user=user,
            defaults = {
                "token": fcm_data.get('token'),
                "device_type": fcm_data.get('device_type'),
                "os": fcm_data.get('os'),
                "browser": fcm_data.get('browser')
        }
        )


    def post(self, request, *args, **kwargs):
        serializer = UserSignInSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)

            if serializer.validated_data.get('fcm'):
                self.handle_fcm_token_generate(user, serializer.validated_data.get("fcm"))

            return success_response(message="login successful", data={
                                        "refresh": str(refresh),
                                        "access": str(refresh.access_token),
                                        "user": UserSerializer(user).data
            },status_code=status.HTTP_200_OK)


class SignOUTAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        fcm_tokens = FCMToken.objects.filter(user=request.user)
        fcm_tokens.delete()
        return success_response(message='logout successfully', status_code=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serialize = UserSerializer(request.user)
        return success_response(message="User profile get successfully", data=serialize.data, status_code=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serialize = UserSerializer(request.user, data=request.data, partial=True)
        if serialize.is_valid(raise_exception=True):
            serialize.save()
            return success_response(message="User profile update successfully", status_code=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return success_response(message="User account delete successfully", status_code=status.HTTP_200_OK)


class UserChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serialize = ChangePasswordSerializer(data = request.data)
        if serialize.is_valid(raise_exception=True):
            if request.user.check_password(serialize.validated_data["current_password"]):
                user = request.user
                user.set_password(serialize.validated_data["new_password"])
                user.save()
                return success_response(message="Password change successfully", status_code=status.HTTP_200_OK)
            return error_response(message="Incorrect current password", status_code=status.HTTP_400_BAD_REQUEST)


class UserRequestForgotPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serialize = ForgotPasswordsSerializer(data = request.data)
        if serialize.is_valid(raise_exception=True):
            user = serialize.validated_data['user']

            send_forget_password_otp(username=f'{user.username}', user_email=user.email)

            return success_response(message="Forgot password verification mail sent successfully", status_code=status.HTTP_200_OK)


class ValidateForgetPasswordOtpAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serialize = ForgotOtpVerificationSerializer(data = request.data)
        if serialize.is_valid(raise_exception=True):
            user = serialize.validated_data['user']

            resend = request.query_params.get('resend')

            if str(resend).lower() == 'true':
                send_forget_password_otp(username=user.username, user_email=user.email)
                return success_response(message="OTP resent successfully")

            cache_otp = cache.get(f"forget_otp_{user.email}")

            if cache_otp is None:
                return error_response(
                    message="OTP expired, please resend",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if str(cache_otp) == str(serialize.validated_data['otp']):
                return success_response(
                    message="OTP verified successfully",
                    status_code=status.HTTP_200_OK
                )

            return error_response(
                message="Invalid OTP please check your mail",
                status_code=status.HTTP_400_BAD_REQUEST
            )


class ResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serialize = ResetPasswordSerializer(data = request.data)
        if serialize.is_valid(raise_exception=True):
            user = serialize.validated_data['user']
            user.set_password(serialize.validated_data['new_password'])
            user.save()
            return success_response(message='Password reset successfully', status_code=status.HTTP_200_OK)
        else:
            return error_response(message='incorrect password', status_code=status.HTTP_400_BAD_REQUEST)


class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return success_response(message="user account delete successfully", status_code=status.HTTP_200_OK)


class UserFollowAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serialize = UserFollowSerializer(data=request.data)
        if serialize.is_valid(raise_exception=True):
            following_user = serialize.validated_data['following']
            user = request.user

            if user == following_user:
                return error_response(message='you can not follow yourself', status_code=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.filter(follower=request.user, following=following_user)

            if follow.exists():
                follow.delete()
                return success_response(message='Unfollow successfully', status_code=status.HTTP_200_OK)

            Follow.objects.create(follower=user, following=following_user)

            return success_response(message='follow successfully', status_code=status.HTTP_200_OK)


class UserFollowListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        followers = Follow.objects.filter(following=user)
        following = Follow.objects.filter(follower=user)

        return success_response(
            message='follow fetched successfully',
            data={
                "followers_count": followers.count(),
                "following_count": following.count(),
                "followers": UserFollowSerializer(followers, many=True).data,
                "following": UserFollowSerializer(following, many=True).data,
            },
            status_code=status.HTTP_200_OK
        )