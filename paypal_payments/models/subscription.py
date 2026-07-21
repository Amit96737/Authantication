from django.db import models
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator
from users.models.users import User

class SubscriptionPlan(CommonFields):
    PLAN_VALIDITY=(
        ('Free', 'Free'),
        ('Year', 'Year'),
        ('Month', 'Month'),
        ('Week', 'Week'),
        ('Day', 'Day'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_pic = models.ImageField(upload_to="plan", null=True, blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic'])
                                                ])
    validity = models.CharField(max_length=120, choices=PLAN_VALIDITY, null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title