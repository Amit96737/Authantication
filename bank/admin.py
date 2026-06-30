from django.contrib import admin
from bank.models.bank import BankName
from bank.models.account import BankAccount

class BankNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ifsc_code')

admin.site.register(BankName, BankNameAdmin)

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'account_number', 'customer_name', 'phone_number', 'email', 'gender', 'bank', 'aadhar_number')

admin.site.register(BankAccount, BankAccountAdmin)
