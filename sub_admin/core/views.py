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
from bank.models.identity_verification import Identification
from bank.core.services import send_accept_verification_email, send_reject_verification_email
from payments.core.forms import ItemForm


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


@sub_admin_required
def update_user(request, id):
    pass


@sub_admin_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        return redirect('user_management')

    return redirect('user_management')


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
def crud_user_delete(request, id):
    user = get_object_or_404(Student, id=id)

    if request.method == "POST":
        user.delete()
        return redirect('crud_management')

    return redirect('crud_management')

@sub_admin_required
def bank_management(request):
    query = request.GET.get('q')
    bank_record = BankAccount.objects.filter(account_status=True).exclude(id=request.user.id).order_by('-id')


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


def identity_verification(request):
    query = request.GET.get('q')
    document = Identification.objects.filter(verification_status='Pending').exclude(id=request.user.id).order_by('-id')

    if query:
        document = document.filter(
            Q(customer__customer_name__icontains=query) |
            Q(customer__email__icontains=query) |
            Q(customer__account_number__icontains=query)
        )

    paginator = Paginator(document, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'sub_admin/identity_verification.html', {'page_obj': page_obj,})


def approve_verification(request, id):
    if request.method == "POST":
        user = Identification.objects.get(id=id)
        user.verification_status = 'Approved'
        user.customer.account_status = True
        user.customer.save()
        user.save()

        try:
            send_accept_verification_email(user.customer)
        except Exception as e:
            print(f"Email error: {e}")
            messages.warning(request, "Verification approve, but we faced an issue sending the verification email.")

        messages.success(request, "Verification approve successfully")
    return redirect('identity_verification')


def reject_verification(request, id):
    if request.method == "POST":
        user = Identification.objects.get(id=id)

        reason = request.POST.get("reason")

        user.verification_status = 'Rejected'
        user.reject_reason = reason

        user.customer.account_status = False
        user.customer.save()
        user.save()

        try:
            send_reject_verification_email(user.customer, reason)
        except Exception as e:
            print("Email error:", e)
            messages.warning(request, "Verification reject, but we faced an issue sending the verification email.")

        messages.error(request, "Verification rejected successfully")
    return redirect('identity_verification')


@sub_admin_required
def bank_user_delete(request, id):
    user = get_object_or_404(BankAccount, id=id)

    if request.method == "POST":
        user.delete()
        return redirect('bank_management')

    return redirect('bank_management')

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
def update_item_detail(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('stripe_management')
    else:
        form = ItemForm(instance=item)

    return render(request, 'sub_admin/update_item_detail.html', {
        'form': form,
        'item': item
    })

def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Item add successfully")
    else:
        form = ItemForm()

    return render(request, 'sub_admin/add_item.html', locals())


@sub_admin_required
def item_delete(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        item.delete()
        return redirect('stripe_management')

    return redirect('stripe_management')

from payments.models.product import ItemImage
@sub_admin_required
def item_detail(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        images = request.FILES.getlist('extra_images')

        for img in images:
            ItemImage.objects.create(item=item, image=img)

        messages.success(request, "Image add successfully")
    return render(request, 'sub_admin/item_detail.html', {
        'item': item
    })


@sub_admin_required
def update_item_detail(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('stripe_management')
    else:
        form = ItemForm(instance=item)

    return render(request, 'sub_admin/update_item_detail.html', {
        'form': form,
        'item': item
    })


@sub_admin_required
def paypal_management(request):
    return render(request, 'sub_admin/paypal_management.html', locals())


@sub_admin_required
def sub_admin_settings(request):
    return render(request, 'sub_admin/settings.html', locals())