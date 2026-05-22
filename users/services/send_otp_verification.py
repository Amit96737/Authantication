from  django.template.loader import render_to_string
import random
from django.core.cache import cache
from datetime import datetime
from users.task import auth_mail_send
from users.task import send_sms

def send_otp_to_mail(username, user_email):
    otp = random.randint(100000, 999999)
    print("email_otp", otp)
    html_message = render_to_string('mail/otp_verification.html', {
        'username': username.title(),
        'otp': otp,
        "year": str(datetime.now().year)
    })
    cache.set(f"otp_{user_email}", otp, 60*10)
    subject = 'OTP for Verification'
    auth_mail_send.delay(subject, html_message, user_email)


def send_otp_to_phone(username,phone_number):
    otp = random.randint(100000, 999999)
    print("sms_otp", otp)
    cache.set(f"sms_otp_{phone_number}", otp, 60*10)

    sms_body = f"""
        Hello {username} from Authentication system ! Your one-time password (OTP) is: {otp}. It will expire in 10 minutes. Do not share this code with anyone.
        """
    send_sms.delay(phone_number, sms_body)

def send_forget_password_otp(username, user_email):
    otp = random.randint(100000, 999999)
    print("forgot_otp", otp)

    html_message = render_to_string('mail/otp_verification.html', {
        'username': username.title(),
        'otp': otp,
        "year": str(datetime.now().year)
    })

    cache.set(f"forget_otp_{user_email}", otp, 60*10)
    subject = 'Forgot password email verification'
    auth_mail_send.delay(subject, html_message, user_email)
