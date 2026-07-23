from django.db import models
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator
from users.models.users import User

class Item(CommonFields):
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=120)
    description = models.CharField(max_length=350)
    image = models.ImageField(upload_to="item_image", null=True, blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'jfif'])
                                                ])
    price = models.DecimalField(max_digits=20, decimal_places=2)
    colors = models.CharField(max_length=120)
    size = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    is_sold = models.BooleanField(default=False)

class FavouriteItem(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'item')

