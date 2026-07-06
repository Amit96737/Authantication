from django.contrib import admin
from payments.models.product import Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'description', 'price', 'colors','size', 'category', 'is_sold')

admin.site.register(Item, ItemAdmin)
