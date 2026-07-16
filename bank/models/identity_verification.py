from django.db import models
from bank.models.account import BankAccount
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator


class Identification(CommonFields):
    customer = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='identity_verification')

    middle_mark_sheet = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg'])
                                       ])
    secondary_mark_sheet = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg'])
                                   ])
    aadhar_image = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg'])
                                       ])
    pan_card = models.ImageField(upload_to='identity_verification', null=True, blank=True,
                                   validators=[
                                       FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'svg'])
                                       ])

    verification_status = models.BooleanField(default=False)
