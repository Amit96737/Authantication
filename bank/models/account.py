from django.db import models
from common.models.common import CommonFields
from users.services.validations import validate_phone_number
from bank.models.bank import BankName
from bank.core.services import generate_account_number

class BankAccount(CommonFields):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    account_number = models.IntegerField(default=generate_account_number, unique=True, editable=False)
    customer_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, validators=[validate_phone_number])
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=255, choices=gender_choices, null=True, blank=True)
    bank = models.ForeignKey(BankName, on_delete=models.CASCADE)
    address = models.TextField()
    aadhar_number = models.CharField(max_length=12, unique=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    account_status = models.BooleanField(default=False)
