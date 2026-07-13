import uuid
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.services.validations import validate_phone_number
from users.models.user_manager import UserManager

class User(AbstractUser):
    gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    )

    id = models.CharField(primary_key=True, default=uuid.uuid4, unique=True, editable=False, max_length=255)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="user_profile", null=True, blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg'])
                                                ])
    gender = models.CharField(max_length=255, choices=gender_choices)
    biograph = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, validators=[validate_phone_number])
    email_verified = models.BooleanField(default=False)
    sms_verified = models.BooleanField(default=False)
    has_subscription = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    objects = UserManager()

