from django.shortcuts import redirect
import csv
from django.http import HttpResponse
from users.models.users import User
from payments.models.product import Item


def sub_admin_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated and (getattr(request.user, 'is_sub_admin', False) or request.user.is_staff):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_sign_up')
    return _wrapped_view_func


def download_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)

    writer.writerow(['ID', 'First Name', 'Last Name', 'Email Address', 'Gender', 'Phone Number', 'Created At', 'Status'])

    users = User.objects.all()

    for user in users:
        writer.writerow([
            user.id,
            user.first_name,
            user.last_name,
            user.email,
            user.gender,
            user.phone_number,
            user.date_joined,
            user.is_active,
        ])

    return response


def download_items_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="items.csv"'

    writer = csv.writer(response)

    writer.writerow(['ID', 'title', 'brand', 'description', 'price', 'colors', 'size', 'category', 'is_sold'])

    items_data = Item.objects.all()

    for item in items_data:
        writer.writerow([
            item.id,
            item.title,
            item.brand,
            item.description,
            item.price,
            item.colors,
            item.size,
            item.category,
            item.is_sold
        ])

    return response