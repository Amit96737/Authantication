from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sub_admin.core.services import sub_admin_required
from users.models.users import User
from crud.models.student import Student
from bank.models.account import BankAccount
from bank.models.bank import BankName
from payments.models.product import Item

@login_required(login_url='user_login')
@sub_admin_required
def sub_admin_dashboard(request):
    total_dev_users = User.objects.all().count()
    total_students = Student.objects.all().count()
    total_banks_account = BankAccount.objects.count()
    total_items = Item.objects.all().count()
    total_subscription = User.objects.filter(has_subscription=True).count()
    total_register_bank = BankName.objects.all().count()
    return render(request, 'sub_admin/dashboard.html', locals())