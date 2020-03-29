from django.core.mail import EmailMessage
from recipeApp.settings import *


def send_email(to_list, subject, message, sender=EMAIL_HOST_USER):
    msg = EmailMessage(subject, message, sender, to_list)
    msg.content_subtype = "html"
    return msg.send()
