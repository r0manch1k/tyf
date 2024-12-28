import os
import uuid
import random
import string
import hashlib
from django.conf import settings
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator


SALT = os.urandom(32)


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


def getHash(data: str):
    return hashlib.pbkdf2_hmac("sha256", data.encode("utf-8"), SALT, 100000).hex()


def generateVerifyToken(data: str):
    return uuid.uuid5(
        namespace=uuid.NAMESPACE_URL,
        name=data,
    ).hex

AccountActivationToken = PasswordResetTokenGenerator()
