import random
import string
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def generateOTP(length=6):
    characters = string.digits
    otp = "".join(random.choice(characters) for _ in range(length))
    return otp


def sendEmail(user, otp, reset_password=False, register_cofirm=False):
    if reset_password:
        subject = "Reset Password - Tell Your Friends"
        context = "reset your password"
    elif register_cofirm:
        subject = "Confirm Registration - Tell Your Friends"
        context = "confirm registration"
    else:
        return

    html_content = render_to_string(
        "otp/emailTemplate.html", {"context": context, "otp_key": otp}
    )

    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        subject, text_content, settings.EMAIL_HOST_USER, [user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
