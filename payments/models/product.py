from django.db import models
from common.models.common import CommonFields
from django.core.validators import FileExtensionValidator
from users.models.users import User
from tinymce.models import HTMLField

class Item(CommonFields):
    title = models.CharField(max_length=250)
    brand = models.CharField(max_length=120)
    description = HTMLField(null=True, blank=True)
    image = models.ImageField(upload_to="item_image", null=True, blank=True,
                                    validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'jfif'])
                                                ])
    price = models.DecimalField(max_digits=20, decimal_places=2)
    colors = models.CharField(max_length=120)
    size = models.CharField(max_length=120)
    category = models.CharField(max_length=120)
    is_sold = models.BooleanField(default=False)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    @property
    def discount_percentage(self):
        if self.mrp and self.price and self.mrp > self.price:
            return int(((self.mrp-self.price) / self.mrp) * 100)
        return 0

    def __str__(self):
        return self.title

class FavouriteItem(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'item')

class ItemImage(CommonFields):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    image = models.ImageField(
        upload_to="item_images",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'jfif'])]
    )

    def __str__(self):
        return self.item.title

class Cart(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)