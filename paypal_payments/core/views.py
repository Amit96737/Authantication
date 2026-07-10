from django.shortcuts import render, redirect, get_object_or_404
from paypal_payments.models.subscription import SubscriptionPlan
import requests
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

CLIENT_ID = settings.PAYPAL_CLIENT_ID
SECRET = settings.PAYPAL_SECRET_KEY

def paypal_about_page(request):
    return render(request, 'paypal/paypal_about_page.html', locals())

def plan_page(request):
    plans = SubscriptionPlan.objects.all()
    context = {
            'plans': plans,
        }
    return render(request, 'paypal/paypal_home.html', context)

def get_paypal_access_token():
    auth = (CLIENT_ID, SECRET)
    data = {'grant_type': 'client_credentials'}
    response = requests.post(
        'https://api-m.sandbox.paypal.com/v1/oauth2/token',
        auth=auth,
        data=data
    )
    return response.json()['access_token']


def initiate_paypal_payment(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    access_token = get_paypal_access_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": str(plan.price)
            },
            "description": plan.title,
            "custom_id": str(request.user.id)
        }],
        "application_context": {
            "return_url": f"{settings.DOMAIN_NAME}/paypal_payments/paypal-payment-success/",
            "cancel_url": f"{settings.DOMAIN_NAME}/paypal_payments/paypal-payment-cancelled/"
        }
    }

    response = requests.post(
        'https://api-m.sandbox.paypal.com/v2/checkout/orders',
        json=order_data,
        headers=headers
    )

    order_info = response.json()

    if 'links' in order_info:
        for link in order_info['links']:
            if link['rel'] == 'approve':
                paypal_redirect_url = link['href']
                return redirect(paypal_redirect_url)

    return HttpResponse("Error processing PayPal redirection layer.", status=400)


def payment_success_view(request):
    token = request.GET.get('token')

    if not token:
        return HttpResponse("Order token missing.", status=400)

    access_token = get_paypal_access_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    capture_url = f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{token}/capture'
    capture_response = requests.post(capture_url, headers=headers)
    capture_data = capture_response.json()

    if capture_data.get('status') == 'COMPLETED':
        context = {
            'order_id': token,
            'payer_name': capture_data.get('payer', {}).get('name', {}).get('given_name', 'Customer')
        }
        return render(request, 'paypal/paypal_success.html', context)

    return HttpResponse(f"Capture failed or already processed. Details: {capture_data}", status=400)

def payment_cancelled_view(request):
    return render(request, 'paypal/paypal_cancelled.html')

@csrf_exempt
def paypal_webhook(request):
    if request.method == 'POST':
        try:
            event_data = json.loads(request.body.decode('utf-8'))
            event_type = event_data.get('event_type')

            if event_type == 'PAYMENT.CAPTURE.COMPLETED':
                resource = event_data.get('resource', {})

                user_id = resource.get('custom_id')

                if user_id:
                    from users.models.users import User
                    user = User.objects.get(id=user_id)
                    user.has_subscription = True
                    user.save()

                return HttpResponse("Webhook received successfully", status=200)

        except Exception as e:
            print("Webhook Error:", str(e))
            return HttpResponse("Error processing webhook", status=400)

    return HttpResponse("Invalid request method", status=405)