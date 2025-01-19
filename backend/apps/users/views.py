import requests
from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    SetPasswordSerializer,
    ResetPasswordSerializer,
    SocialLoginSerializer,
)
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
from apps.profiles.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .permissions import VerificationPermissions
from rest_framework.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


User = get_user_model()


class SocialLogin(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SocialLoginSerializer

    def post(self, request, social):
        try:
            token = request.data.get("access_token")

            if social == "google":
                response = requests.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo",
                    headers={"Authorization": f"Bearer {token}"},
                )
                if response.status_code != status.HTTP_200_OK:
                    return Response(
                        {
                            "message": "Что-то пошло не так, повторите попытку позже.",
                            "payload": {},
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

                userInfo = response.json()
                email = userInfo.get("email", "")
                username = userInfo.get("name", "")
                firstName = userInfo.get("given_name", "")
                lastName = userInfo.get("given_name", "")
                avatarUrl = userInfo.get("picture", "")

            elif social == "yandex":
                response = requests.get(
                    "https://login.yandex.ru/info",
                    headers={"Authorization": f"Bearer {token}"},
                    params={"format": "json"},
                )
                if response.status_code != status.HTTP_200_OK:
                    return Response(
                        {"error": "Authentication forbidden"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                userInfo = response.json()
                email = userInfo.get("default_email", "")
                username = userInfo.get("display_name", "")
                firstName = userInfo.get("first_name", "")
                lastName = userInfo.get("last_name", "")
                avatarId = userInfo.get("default_avatar_id", "")
                avatarUrl = (
                    f"""https://avatars.yandex.net/get-yapic/{avatarId}/islands-200"""
                    if avatarId
                    else ""
                )

            else:
                return Response(
                    {
                        "message": "Источник не был определён.",
                        "payload": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            isExists = User.objects.filter(email=email).exists()
            isSocialUser = (
                User.objects.get(email=email).is_social_user if isExists else False
            )

            if not isExists:
                serializer = self.get_serializer(data={"email": email})
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                profile = Profile.objects.get(email=email)
                profile.username = username
                profile.first_name = firstName
                profile.last_name = lastName
                if avatarUrl:
                    profile.save_avatar_from_url(avatarUrl)
                profile.save()

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

            elif isExists and isSocialUser:
                user = User.objects.get(email=email)
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

            else:
                return Response(
                    {
                        "message": "Пользователь с таким адресом эл. почты уже зарегистрирован. Войдите в ваш аккаунт.",
                        "payload": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except BaseException:
            return Response(
                {
                    "message": "Что-то пошло не так, повторите попытку позже.",
                    "payload": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )


class Login(GenericAPIView):
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
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
    permission_classes = [AllowAny]
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

            user = User.objects.get(pk=force_str(urlsafe_base64_decode(uid)))
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

        except BaseException:
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

        return Response(
            {
                "message": gettext("Новый код был отправлен на адрес вашей эл. почты!"),
                "payload": {},
            },
            status=status.HTTP_200_OK,
        )
