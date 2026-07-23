from django.shortcuts import render, redirect
from payments.models.product import Item, FavouriteItem
import stripe
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_about_page(request):
    return render(request, "payments/stripe_about_page.html", locals())

def item_detail(request):
    items = Item.objects.filter(is_sold=False)
    fav_items=[]
    if request.user.is_authenticated:
        fav_items = FavouriteItem.objects.filter(user=request.user).values_list('item_id', flat=True)
    return render(request, "payments/product_list.html", {"items": items, 'fav_items': fav_items})


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
                    'description': item.description,
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
    return render(request, "payments/item_detail.html",
                  {
                      "item": item
                  }
                  )