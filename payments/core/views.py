from django.shortcuts import render, redirect
from payments.models.product import Item, FavouriteItem, Cart, Rating
import stripe
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_about_page(request):
    return render(request, "payments/stripe_about_page.html", locals())


def item_detail(request):
    query = request.GET.get('q')
    items = Item.objects.filter(is_sold=False)

    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(colors__icontains=query) |
            Q(category__icontains=query)
        )

    fav_items = []
    if request.user.is_authenticated:
        fav_items = FavouriteItem.objects.filter(user=request.user)\
                        .values_list('item_id', flat=True)

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    return render(request, "payments/product_list.html", {
        "items": items,
        "fav_items": fav_items,
        "cart_count": cart_count
    })


def success(request):
    return render(request, "payments/success.html")

def cancel(request):
    return render(request, "payments/cancel.html")

def create_checkout_session(request, id):
    item = Item.objects.get(id=id)

    quantity = int(request.POST.get("quantity", 1))

    base_url = settings.BASE_URL

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': item.title,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': quantity,
        }],
        mode='payment',
        success_url=f'{base_url}/payments/success/',
        cancel_url=f'{base_url}/payments/cancel/',
        metadata={
            'item_id': str(item.id)
        }
    )

    return redirect(session.url)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        print("Webhook Error:", e)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_dict = session.to_dict()

        metadata = session_dict.get('metadata', {})
        item_id = metadata.get('item_id')

        if not item_id:
            try:
                line_items = session_dict.get('line_items', {}).get('data', [])
                if line_items:
                    item_id = line_items[0].get('price', {}).get('product', {}).get('metadata', {}).get('item_id')
            except Exception:
                pass

        if item_id:
            from payments.models.product import Item
            try:
                item = Item.objects.get(id=item_id)
                item.is_sold = True
                item.save()
                # print(f"Success: Item {item_id} marked as sold!")
            except Item.DoesNotExist:
                print(f"Error: Item ID {item_id} not present in database.")
        else:
            # print("Error: under Metadata not item_id")
            print("Stripe metadata: ", metadata)

    return HttpResponse(status=200)


def favourite_items(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login')

    item = Item.objects.get(id=id)
    fav_item = FavouriteItem.objects.filter(user=request.user, item=item)

    if fav_item.exists():
        fav_item.delete()
        return JsonResponse({'status': 'removed'})
    else:
        FavouriteItem.objects.create(user=request.user, item=item)
        return JsonResponse({'status': 'added'})


def specific_item_detail(request, id):
    item = Item.objects.get(id=id)

    related_items = Item.objects.filter(
        category=item.category,
        is_sold=False
    ).exclude(id=item.id)[:3]

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    rating_data = Rating.objects.filter(item=item).aggregate(
        avg_rating=Avg('rating'),
        total_ratings=Count('id')
    )

    avg_rating = rating_data['avg_rating'] or 0

    user_rating = None
    if request.user.is_authenticated:
        rating_obj = Rating.objects.filter(
            user=request.user,
            item=item
        ).first()

        if rating_obj:
            user_rating = rating_obj.rating

    return render(request, "payments/item_detail.html", {
        "item": item,
        "related_items": related_items,
        "cart_count": cart_count,
        "user_rating": user_rating,
        "avg_rating": avg_rating
    })


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        item=item
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Item added to cart successfully")
    return redirect('specific_item_detail', id=item.id)

def cart_page(request):
    query = request.GET.get('q')
    cart_items = Cart.objects.filter(user=request.user)

    if query:
        cart_items = cart_items.filter(
            Q(item__title__icontains=query) |
            Q(item__brand__icontains=query) |
            Q(item__description__icontains=query) |
            Q(item__colors__icontains=query) |
            Q(item__category__icontains=query)
        )

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    return render(request, "payments/cart.html", {"cart_items": cart_items,
                                                  "cart_count": cart_count})

def favourite_item_page(request):
    query = request.GET.get('q')
    fav_items = FavouriteItem.objects.filter(user=request.user)

    if query:
        fav_items = fav_items.filter(
            Q(item__title__icontains=query) |
            Q(item__brand__icontains=query) |
            Q(item__description__icontains=query) |
            Q(item__colors__icontains=query) |
            Q(item__category__icontains=query)
        )

    return render(request, "payments/favourite.html", {
        "fav_items": fav_items
    }
                  )

def delete_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart_page')

def delete_favourite_item(request, id):
    fav_item = get_object_or_404(FavouriteItem, id=id, user=request.user)
    fav_item.delete()
    return redirect('favourite_item_page')

def checkout_page(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, "payments/checkout.html", {"item": item})


def trending_items(request):
    query = request.GET.get('q')
    trending_items = Item.objects.annotate(
        fav_count=Count('favouriteitem')
    ).filter(fav_count__gt=2).order_by('-fav_count')

    if query:
        trending_items = trending_items.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(colors__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, "payments/trending.html", {
        "trending_items": trending_items
    })


def new_releases(request):
    query = request.GET.get('q')
    three_days_ago = timezone.now() - timedelta(days=5)
    new_item = Item.objects.filter(is_active=True, created_at__gte=three_days_ago)
    if query:
        new_item = new_item.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(colors__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, "payments/new_releases.html", {
        "new_item": new_item
    })

def rating(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        rating_value = int(request.POST.get("rating"))

        Rating.objects.update_or_create(
            user=request.user,
            item=item,
            defaults={"rating": rating_value}
        )

    return redirect('specific_item_detail', id=item.id)
