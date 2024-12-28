from django.contrib import auth
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from django.core.cache import cache
from apps.utils.verifyTools import (
    generateOTP,
    sendEmail,
    getHash,
    generateVerifyToken,
    AccountActivationToken,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .permissions import VerificationPermissions
from rest_framework.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


User = get_user_model()


class Login(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = auth.authenticate(
                email=request.data.get("email"), password=request.data.get("password")
            )
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({"user_id": user.id, "email": user.email})

            return Response(
                {
                    "message": "OK",
                    "payload": {
                        "token": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                    },
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            if e.detail.keys().__contains__("password"):
                error = e.detail.get("password")[0].capitalize()
            elif e.detail.keys().__contains__("email"):
                error = e.detail.get("email")[0].capitalize()
            elif e.detail.keys().__contains__("info"):
                error = e.detail.get("info")[0].capitalize()
            else:
                error = "Something went wrong, please try again later."

            return Response(
                {"message": error, "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Logout(APIView):
    def post(self, request):
        raw_token = request.data.get("token")
        if not raw_token:
            return Response(
                {"message": "Token is required.", "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(raw_token.get("refresh"))
            refresh.blacklist()
        except TokenError:
            return Response(
                {"message": "Token is invalid.", "payload": {}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response({"message": "OK", "payload": {}}, status=status.HTTP_200_OK)


class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            if User.objects.filter(email=request.data.get("email")).exists():
                if not User.objects.get(email=request.data.get("email")).is_active:
                    user = User.objects.get(email=request.data.get("email"))

                    verify_token = generateVerifyToken(
                        f"""{request.META.get("REMOTE_ADDR")}-{user.email}-{user.pk}"""
                    )
                    redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                        token=getHash(verify_token)
                    )
                    if cache.get(redis_key) is None:
                        cache.delete(redis_key)

                    user = User.objects.get(email=request.data.get("email"))
                    user.delete()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            verify_token = generateVerifyToken(
                f"""{request.META.get("REMOTE_ADDR")}-{user.email}-{user.pk}"""
            )
            redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                token=getHash(verify_token)
            )
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            cache.set(
                key=redis_key,
                value={
                    "user_token": AccountActivationToken.make_token(user=user),
                },
                timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
            )

            otp = generateOTP()
            user.otp = getHash(otp)
            sendEmail(user=user, otp=otp, reset_password=False, register_cofirm=True)

            user.save()

            return Response(
                {
                    "message": "OK",
                    "payload": {
                        "token": verify_token,
                        "uid": uid,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            if e.detail.keys().__contains__("password1"):
                error = e.detail.get("password1")[0].capitalize()
            elif e.detail.keys().__contains__("email"):
                error = e.detail.get("email")[0].capitalize()
            elif e.detail.keys().__contains__("info"):
                error = e.detail.get("info")[0].capitalize()
            else:
                error = "Something went wrong, please try again later."

            return Response(
                {"message": error, "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except BaseException:
            return Response(
                {
                    "message": "Something went wrong, please try again later.",
                    "payload": {},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Verification(APIView):
    permission_classes = [VerificationPermissions]

    def get(self, request):
        return Response(
            {
                "message": "OK",
                "payload": {},
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def post(self, request):
        user = User.objects.get(
            pk=force_str(urlsafe_base64_decode(request.data.get("uid")))
        )

        otp = request.data.get("otp", "")
        if user.otp == getHash(str(otp)):
            time_difference = max(user.created_at, user.updated_at)
            mins_difference = (timezone.now() - time_difference).total_seconds() / 60
            if mins_difference >= 1:
                return Response(
                    {"message": "OTP code expired. Try again.", "payload": {}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_active = True
            user.otp = None
            user.save()

            cache.delete(
                settings.TYF_USER_VERIFICATION_KEY.format(
                    token=getHash(request.data.get("token"))
                )
            )

            return Response(
                {"message": "Account verified successfully", "payload": {}},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid OTP.", "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request):
        user = User.objects.get(
            pk=force_str(urlsafe_base64_decode(request.data.get("uid")))
        )
        
        if user.otp is None:
            return Response(
                {
                    "message": "Your account does not require email verification",
                    "payload": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = generateOTP()
        user.otp = getHash(otp)
        user.save()
        sendEmail(user=user, otp=otp, reset_password=False, register_cofirm=True)

        response = {
            "message": "New code has been sent to your email!",
            "payload": {},
        }
        return Response(response, status=status.HTTP_200_OK)
