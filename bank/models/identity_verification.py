from django.db import models
from bank.models.account import BankAccount
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator


class Identification(CommonFields):

    status_choices = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    customer = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='identity_verification')

    middle_mark_sheet = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg', 'jfif'])
                                       ])
    secondary_mark_sheet = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg', 'jfif'])
                                   ])
    aadhar_image = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg', 'jfif'])
                                       ])
    pan_card = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg', 'jfif'])
                                       ])

    verification_status = models.CharField(max_length=120, choices=status_choices, default='Pending')
    reject_reason = models.TextField(null=True, blank=True)
