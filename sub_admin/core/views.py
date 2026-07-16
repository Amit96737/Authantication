from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from sub_admin.core.services import sub_admin_required
from users.models.users import User
from crud.models.student import Student
from bank.models.account import BankAccount
from bank.models.bank import BankName
from payments.models.product import Item
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse


def approve_user(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.status = 'Approved'
        user.is_verified = True
        user.save()
        messages.success(request, "Request accepted successfully")
    return redirect('users_verification')


def reject_user(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)

        reason = request.POST.get("reason")

        user.status = 'Rejected'
        user.reject_reason = reason
        user.save()
        user.is_verified = False
        user.save()
        messages.error(request, "Request rejected successfully")
    return redirect('users_verification')


def sub_admin_user(request):
    query = request.GET.get('q')
    sub_admin = User.objects.filter(is_sub_admin=True).exclude(id=request.user.id).order_by('-id')


    if query:
        sub_admin = sub_admin.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(gender__icontains=query) |
            Q(phone_number__icontains=query)
        )

    paginator = Paginator(sub_admin, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/sub_admin.html', locals())


def toggle_sub_admin(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, id=id)

        user.is_sub_admin = not user.is_sub_admin
        user.save()

        return JsonResponse({
            "status": "success",
            "is_sub_admin": user.is_sub_admin
        })


@sub_admin_required
def users_verification(request):
    query = request.GET.get('q')
    users = User.objects.filter(status='Pending').exclude(id=request.user.id).order_by('-id')

    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(gender__icontains=query) |
            Q(phone_number__icontains=query)
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/users_verification.html', {'page_obj': page_obj,})


@login_required(login_url='user_login')
@sub_admin_required
def sub_admin_dashboard(request):
    total_dev_users = User.objects.exclude(id=request.user.id).count()
    total_students = Student.objects.all().count()
    total_banks_account = BankAccount.objects.count()
    total_items = Item.objects.all().count()
    total_subscription = User.objects.filter(has_subscription=True).count()
    total_register_bank = BankName.objects.all().count()
    return render(request, 'sub_admin/dashboard.html', locals())


@sub_admin_required
def user_management(request):
    query = request.GET.get('q')
    users = User.objects.exclude(id=request.user.id).order_by('-id')

    if query:
        query = query.lower()

        if query == "active":
            users = users.filter(is_active=True)

        elif query == "inactive":
            users = users.filter(is_active=False)

        else:

            users = users.filter(
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(gender__icontains=query) |
                Q(phone_number__icontains=query)
            )

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/user_management.html', {
        'page_obj': page_obj,
    })


@sub_admin_required
def user_detail(request, id):
    selected_user = get_object_or_404(User, id=id)

    return render(request, 'sub_admin/user_profile.html', {
        'selected_user': selected_user
    })


# @sub_admin_required
# def update_user(request, id):
#     user = User.objects.get(id=id)
#
#     if request.method == "POST":
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.email = request.POST.get('email')
#         user.phone_number = request.POST.get('phone_number')
#         user.gender = request.POST.get('gender')
#         user.biograph = request.POST.get('biograph')
#
#         user.is_sub_admin = True if request.POST.get('is_sub_admin') == 'on' else False
#
#         user.save()
#
#     return redirect('update_user',id=user.id)


@sub_admin_required
def crud_management(request):
    query = request.GET.get('q')
    students = Student.objects.all().order_by('-id')

    if query:
        query = query.lower()

        if query == "active":
            users = students.filter(is_active=True)

        elif query == "inactive":
            users = students.filter(is_active=False)

        else:

            students = students.filter(
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(gender__icontains=query) |
                Q(phone_number__icontains=query)
            )

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/crud_management.html', locals())



@sub_admin_required
def bank_management(request):
    query = request.GET.get('q')
    bank_record = BankAccount.objects.all().order_by('-id')


    if query:
        query = query.lower()

        if query == "active":
            users = bank_record.filter(is_active=True)

        elif query == "inactive":
            users = bank_record.filter(is_active=False)

        else:

            bank_record = bank_record.filter(
                Q(account_number__icontains=query) |
                Q(customer_name__icontains=query) |
                Q(email__icontains=query) |
                Q(gender__icontains=query) |
                Q(bank__name__icontains=query) |
                Q(aadhar_number__icontains=query)
            )

    paginator = Paginator(bank_record, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/bank_management.html', locals())


@sub_admin_required
def stripe_management(request):
    query = request.GET.get('q')
    items = Item.objects.all().order_by('-created_at')

    if query:
        query = query.lower()

        if query == "active":
            users = items.filter(is_active=True)

        elif query == "inactive":
            users = items.filter(is_active=False)

        else:

            items = items.filter(
                Q(title__icontains=query) |
                Q(brand__icontains=query) |
                Q(description=query) |
                Q(price__icontains=query) |
                Q(colors__icontains=query) |
                Q(size__icontains=query) |
                Q(category__icontains=query) |
                Q(is_sold__icontains=query)
            )

    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/stripe_management.html', locals())


@sub_admin_required
def paypal_management(request):
    return render(request, 'sub_admin/paypal_management.html', locals())


@sub_admin_required
def sub_admin_settings(request):
    return render(request, 'sub_admin/settings.html', locals())