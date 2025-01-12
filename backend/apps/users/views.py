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
from django.utils.translation import gettext
from django.contrib.auth import get_user_model
from .permissions import VerificationPermissions
from rest_framework.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    SetPasswordSerializer,
    ResetPasswordSerializer,
)


User = get_user_model()


class Login(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            user = auth.authenticate(
                email=request.data.get("email").lower(),
                password=request.data.get("password"),
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
                error = "Что-то пошло не так, повторите попытку позже."

            error = gettext(error)

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
            email = request.data.get("email").lower()
            if User.objects.filter(email=email).exists():
                if not User.objects.get(email=email).is_active:
                    user = User.objects.get(email=email)

                    verify_token = generateVerifyToken()
                    redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                        token=getHash(
                            f"""{verify_token}-{request.META.get("REMOTE_ADDR")}-{user.email}"""
                        )
                    )
                    if cache.get(redis_key) is None:
                        cache.delete(redis_key)

                    user = User.objects.get(email=email)
                    user.delete()

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            verify_token = generateVerifyToken()
            redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                token=getHash(
                    f"""{verify_token}-{request.META.get("REMOTE_ADDR")}-{user.email}"""
                )
            )
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            cache.set(
                key=redis_key,
                value={
                    "user_token": AccountActivationToken.make_token(user=user),
                    "is_register_confirm": True,
                    "is_reset_password_confirm": False,
                },
                timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
            )

            otp = generateOTP()
            user.otp = getHash(otp)
            sendEmail(user=user, otp=otp, reset_password=False, register_confirm=True)

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
            elif e.detail.keys().__contains__("password2"):
                error = e.detail.get("password2")[0].capitalize()
            elif e.detail.keys().__contains__("email"):
                error = e.detail.get("email")[0].capitalize()
            elif e.detail.keys().__contains__("info"):
                error = e.detail.get("info")[0].capitalize()
            else:
                error = "Something went wrong, please try again later."

            error = gettext(error)

            return Response(
                {"message": error, "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except BaseException:
            error = "Что-то пошло не так, повторите попытку позже."
            return Response(
                {
                    "message": error,
                    "payload": {},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ResetPassword(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email = request.data.get("email").lower()
            user = User.objects.get(email=email)

            verify_token = generateVerifyToken()
            redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                token=getHash(
                    f"""{verify_token}-{request.META.get("REMOTE_ADDR")}-{user.email}"""
                )
            )
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            cache.set(
                key=redis_key,
                value={
                    "user_token": AccountActivationToken.make_token(user=user),
                    "is_register_confirm": False,
                    "is_reset_password_confirm": True,
                },
                timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
            )

            otp = generateOTP()
            user.otp = getHash(otp)
            sendEmail(user=user, otp=otp, reset_password=True, register_confirm=False)

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
            if e.detail.keys().__contains__("email"):
                error = e.detail.get("email")[0].capitalize()
            elif e.detail.keys().__contains__("info"):
                error = e.detail.get("info")[0].capitalize()
            else:
                error = "Что-то пошло не так, повторите попытку позже."

            error = gettext(error)

            return Response(
                {"message": error, "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except BaseException:
            return Response(
                {
                    "message": "Что-то пошло не так, повторите попытку позже.",
                    "payload": {},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SetPassword(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SetPasswordSerializer
    permission_classes = [VerificationPermissions]

    def get(self, _):
        return Response(
            {
                "message": "OK",
                "payload": {},
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            uid = request.query_params.get("uid", "")
            token = request.query_params.get("token", "")

            user = User.objects.get(
                pk=force_str(urlsafe_base64_decode(uid))
            )

            user.set_password(request.data.get("password1"))
            user.save()

            redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                token=getHash(
                    f"""{token}-{request.META.get("REMOTE_ADDR")}-{user.email}"""
                )
            )
            cache.delete(
                settings.TYF_USER_VERIFICATION_KEY.format(token=getHash(redis_key))
            )

            return Response(
                {
                    "message": "Пароль успешно сменён!",
                    "payload": {},
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            if e.detail.keys().__contains__("password1"):
                error = e.detail.get("password1")[0].capitalize()
            elif e.detail.keys().__contains__("password2"):
                error = e.detail.get("password2")[0].capitalize()
            elif e.detail.keys().__contains__("info"):
                error = e.detail.get("info")[0].capitalize()
            else:
                error = "Что-то пошло не так, повторите попытку позже."

            gettext(error)

            return Response(
                {"message": error, "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except BaseException as e:
            return Response(
                {
                    "message": "Что-то пошло не так, повторите попытку позже.",
                    "payload": {},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Verification(APIView):
    permission_classes = [VerificationPermissions]

    def get(self, _):
        return Response(
            {
                "message": "OK",
                "payload": {},
            },
            status=status.HTTP_202_ACCEPTED,
        )

    def post(self, request):
        otp = request.data.get("otp", "")
        uid = request.query_params.get("uid", "")
        token = request.query_params.get("token", "")

        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
        except BaseException:
            return Response(
                {
                    "message": "Invalid uid",
                    "payload": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.otp == getHash(str(otp)):
            time_difference = max(user.created_at, user.updated_at)
            mins_difference = (timezone.now() - time_difference).total_seconds() / 60
            if mins_difference >= 1:
                return Response(
                    {
                        "message": "Ваш код истёк. Запросите новый код и попробуйте снова.",
                        "payload": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not user.is_active:
                user.is_active = True
            user.otp = None
            user.save()

            redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                token=getHash(
                    f"""{token}-{request.META.get("REMOTE_ADDR")}-{user.email}"""
                )
            )
            if cache.get(redis_key)["is_reset_password_confirm"]:
                print("reset password")
                verify_token = generateVerifyToken()
                redis_key = settings.TYF_USER_VERIFICATION_KEY.format(
                    token=getHash(
                        f"""{verify_token}-{request.META.get("REMOTE_ADDR")}-{user.email}"""
                    )
                )
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                cache.set(
                    key=redis_key,
                    value={
                        "user_token": AccountActivationToken.make_token(user=user),
                    },
                    timeout=settings.TYF_USER_VERIFICATION_TIMEOUT,
                )
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
            else:
                cache.delete(redis_key)
                return Response(
                    {
                        "message": "Ваш аккаунт успешно подтверждён",
                        "payload": {},
                    },
                    status=status.HTTP_200_OK,
                )

        else:
            return Response(
                {"message": "Неверный код.", "payload": {}},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request):
        user = User.objects.get(
            pk=force_str(urlsafe_base64_decode(request.query_params.get("uid")))
        )

        if user.otp is None:
            return Response(
                {
                    "message": gettext("Ваш аккаунт не нуждается в подтверждении."),
                    "payload": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        otp = generateOTP()
        user.otp = getHash(otp)
        user.save()
        sendEmail(user=user, otp=otp, reset_password=False, register_confirm=True)
        print(otp)

        response = {
            "message": gettext("Новый код был отправлен на адрес вашей эл. почты!"),
            "payload": {},
        }
        return Response(response, status=status.HTTP_200_OK)
