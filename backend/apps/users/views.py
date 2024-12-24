from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.cache import cache
from social_django.models import UserSocialAuth
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken, TokenError


User = get_user_model()

from apps.utils.otpTools import (
    generateOTP,
    sendEmail,
)


@api_view(["GET"])
def apiOverview(request):
    return Response(
        {
            "Overview": "/api/overview",
            "Login": "/api/login",
            "Register": "/api/register",
            "VerifyOTP": "/api/verify-otp",
            "ResendOTP": "/api/resend-otp",
        }
    )


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if UserSocialAuth.objects.filter(
                user__email=request.data.get("email")
            ).exists():
                return Response(
                    {
                        "message": "User with this Email was registered using Google/Yandex. Please sign in using same method.",
                        "payload": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if User.objects.filter(email=request.data.get("email")).exists():
                if not User.objects.get(email=request.data.get("email")).is_active:
                    user = User.objects.get(email=request.data.get("email"))
                    user.delete()

            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            otp = generateOTP()
            user.otp = otp
            sendEmail(user=user, otp=otp, reset_password=False, register_cofirm=True)
            user.save()

            return Response(
                {
                    "message": "OK",
                    "payload": {
                        "user": {
                            "id": user.id,
                            "email": user.email,
                        },
                        "token": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            if e.detail.keys().__contains__("password1"):
                error = e.detail.get("password1")[0].capitalize()
            elif e.detail.keys().__contains__("info"):
                error = e.detail.get("info")[0].capitalize()
            elif e.detail.keys().__contains__("email"):
                error = e.detail.get("email")[0].capitalize()
            else:
                error = "Something went wrong, please try again later."

            return Response(
                {"message": error, "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class VerifyOTP(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"message": "Token is required.", "payload": {}}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            AccessToken(token.get("access"))
            RefreshToken(token.get("refresh"))
        except TokenError:
            return Response(
                {"message": "Token is invalid.", "payload": {}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = request.data.get("email", "")
        otp = request.data.get("otp", "")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "User with this email does not exist.", "payload": {}},
                status=status.HTTP_404_NOT_FOUND,
            )

        print(user.otp)
        if user.otp == otp:
            time_difference = max(user.created_at, user.updated_at)
            mins_difference = (timezone.now() - time_difference).total_seconds() / 60
            if mins_difference > 1:
                return Response(
                    {"message": "OTP token expired. Try again.", "payload": {}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_active = True
            user.otp = None
            user.save()

            # Authenticate the user and create or get an authentication token
            # token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {"message": "Account verified successfully", "payload": {}},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Invalid OTP.", "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResendOTP(APIView):
    def patch(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"message": "Token is required.", "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            AccessToken(token.get("access"))
            RefreshToken(token.get("access"))
        except TokenError:
            return Response(
                {"message": "Token is invalid.", "payload": {}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist", "payload": {}},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.otp is None:
            return Response(
                {"message": "Your account already verified", "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = generateOTP()
        user.otp = otp
        user.save()
        sendEmail(user=user, otp=otp, reset_password=False, register_cofirm=True)

        response = {
            "message": "New code has been sent to your email!",
            "payload": {},
        }
        return Response(response, status=status.HTTP_200_OK)
