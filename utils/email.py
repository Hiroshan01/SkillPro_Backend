from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail


# Send quick email
@shared_task
def send_email(subject, body, recipient_list):
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


# Send HTML email
@shared_task
def send_html_email(subject, body_html, recipient_list):
    email = EmailMultiAlternatives(
        subject=subject,
        body="Please view this email in an HTML-compatible client.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list,
    )
    email.attach_alternative(body_html, "text/html")
    email.send()
