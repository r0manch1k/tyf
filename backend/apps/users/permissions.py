from django.conf import settings
from django.core.cache import cache
from apps.utils.verifyTools import (
    getHash,
    # generateVerifyToken,
    AccountActivationToken,
)
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from rest_framework.permissions import BasePermission


User = get_user_model()


class VerificationPermissions(BasePermission):
    def has_permission(self, request, view):
        uid = request.data.get("uid")
        incoming_token = request.data.get("token")
        remote_addr = request.META.get("REMOTE_ADDR")

        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            print("0")
            return False

        if not incoming_token:
            print("1")
            return False

        redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
            token=getHash(f"{incoming_token}-{remote_addr}")
        )
        if cache.get(redis_key) is None:
            print("2")
            return False

        redis_data = cache.get(redis_key)
        if not AccountActivationToken.check_token(user, redis_data["user_token"]):
            print("3")
            return False

        return True
