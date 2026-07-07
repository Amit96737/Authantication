from django.contrib import admin
from paypal_payments.models.subscription import SubscriptionPlan

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'validity')

admin.site.register(SubscriptionPlan, SubscriptionAdmin)