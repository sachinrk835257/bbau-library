
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import render, HttpResponse
# from pathlib import Path
from decouple import config


def send_mail(email,subject, message, html_message):
    print("in send mail function")
    recipient_list = [f"{email}"]
    from_email = config('EMAIL_HOST_USER')
    email = EmailMultiAlternatives(subject, message, from_email, recipient_list)
    email.content_subtype = 'html'
    email.attach_alternative(html_message, "text/html")  # Attach HTML content

    # Send the email
    email.send()

    return True