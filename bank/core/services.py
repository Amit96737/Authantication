import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def generate_account_number():
    while True:
        account_number = random.randint(100000000, 999999999)
        return account_number

def send_account_email(account):
    subject = "Account Created Successfully"

    context = {
        'name': account.customer_name,
        'account_number': account.account_number,
        'ifsc': account.bank.ifsc_code,
        'bank': account.bank,
        'aadhar_number': account.aadhar_number,
        'activate_url': f"http://127.0.0.1:8000/bank/activate/{account.id}/",
        'deactivate_url': f"http://127.0.0.1:8000/bank/deactivate/{account.id}/",
    }

    html_content = render_to_string("bank/create_account_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()