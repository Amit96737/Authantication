from django.db import models
from common.models.common import CommonFields
import random
import string

class BankName(CommonFields):
    name = models.CharField(max_length=120)
    ifsc_code = models.CharField(max_length=11, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.upper()

        if not self.ifsc_code:
            bank_part = self.name[:4].ljust(4, 'X')
            random_part = ''.join(random.choices(string.digits, k=7))

            self.ifsc_code = (bank_part + random_part).upper()

        super().save(*args, **kwargs)