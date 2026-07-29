from django.contrib import admin
from payments.models.product import Item, ItemImage, Cart
from payments.models.transaction import Transaction

class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'brand', 'price', 'colors','size', 'category', 'is_sold', 'quantity')

admin.site.register(Item, ItemAdmin)


class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'image')

admin.site.register(ItemImage, ItemImageAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'quantity')

admin.site.register(Cart, CartAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'payment_intent_id', 'amount', 'status')

admin.site.register(Transaction, TransactionAdmin)