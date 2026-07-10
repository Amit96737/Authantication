from django.db import models
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator
from tinymce.models import HTMLField

class Student(CommonFields):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=255, choices=gender_choices)
    profile_pic = models.ImageField(upload_to="student", null=True, blank=True,
                                    validators=[
                                        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])
                                        ])
    address = models.TextField()
    biograph = HTMLField(null=True, blank=True)
    account_status = models.BooleanField(default=False)
