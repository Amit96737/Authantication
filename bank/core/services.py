import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.timezone import now

def generate_account_number():
    while True:
        account_number = random.randint(100000000, 999999999)
        return account_number

def send_accept_verification_email(account):
    subject = "Account Verification Accepted"

    context = {
        'name': account.customer_name,
        'account_number': account.account_number,
        'ifsc': account.bank.ifsc_code,
        'bank': account.bank,
        'aadhar_number': account.aadhar_number
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


def send_reject_verification_email(account, reason):
    subject = "Account Verification Rejected"

    context = {
        'name': account.customer_name,
        'reason': reason,
    }

    html_content = render_to_string("bank/reject_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()



def send_deposit_email(account, amount):
    subject = "Deposit Successful"

    context = {
        "name": account.customer_name,
        "amount": amount,
        "account_number": account.account_number,
        "balance": account.balance,
        "date_time": now().strftime('%d-%m-%Y %H:%M:%S'),
        "bank": account.bank,
    }

    html_content = render_to_string("bank/deposit_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

def send_withdraw_email(account, amount):
    subject = "Withdraw Successful"

    context = {
        "name": account.customer_name,
        "amount": amount,
        "account_number": account.account_number,
        "balance": account.balance,
        "date_time": now().strftime('%d-%m-%Y %H:%M:%S'),
        "bank": account.bank,
    }

    html_content = render_to_string("bank/withdraw_email.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[account.email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

def send_transfer_email(sender, receiver, amount):
    subject = "Amount Transferred"

    date_time = now().strftime('%d-%m-%Y %H:%M:%S')

    sender_context = {
        "name": sender.customer_name,
        "amount": amount,
        "account_number": sender.account_number,
        "balance": sender.balance,
        "receiver_name": receiver.customer_name,
        "date_time": date_time,
        "bank": sender.bank,
    }

    sender_html = render_to_string("bank/transfer_debit_email.html", sender_context)
    sender_text = strip_tags(sender_html)

    sender_email = EmailMultiAlternatives(
        subject="Amount Debited",
        body=sender_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[sender.email],
    )

    sender_email.attach_alternative(sender_html, "text/html")
    sender_email.send()

    receiver_context = {
        "name": receiver.customer_name,
        "amount": amount,
        "account_number": receiver.account_number,
        "balance": receiver.balance,
        "sender_name": sender.customer_name,
        "date_time": date_time,
        "bank": receiver.bank,
    }

    receiver_html = render_to_string("bank/transfer_credit_email.html", receiver_context)
    receiver_text = strip_tags(receiver_html)

    receiver_email = EmailMultiAlternatives(
        subject="Amount Credited",
        body=receiver_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[receiver.email],
    )

    receiver_email.attach_alternative(receiver_html, "text/html")
    receiver_email.send()