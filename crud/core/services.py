from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_verification_email(student):
    subject = "Verify Your Student Account"
    domain = settings.DOMAIN_NAME

    context = {
        'student': student,
        'accept_url': f"{domain}/crud/verify-account/{student.id}/?action=accept",
        'reject_url': f"{domain}/crud/verify-account/{student.id}/?action=reject"
    }

    html_content = render_to_string("student/email_verification.html", context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[student.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()