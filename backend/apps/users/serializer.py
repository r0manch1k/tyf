from django.contrib import auth
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model
from social_django.models import UserSocialAuth
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "email"]

    def validate(self, attrs):
        email = attrs.get("email", "").lower()
        password = attrs.get("password", "")

        if UserSocialAuth.objects.filter(user__email=email).exists():
            raise serializers.ValidationError(
                detail={
                    "info": "Пользователь с этим адресом эл. почты был зарегистрирован с помощью Google/Яндекс. Пожалуйста, войдите в систему, используя тот же метод."
                },
            )

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail={"info": "Пользователь с этим адресом эл. почты не существует"}
            )
        else:
            if not User.objects.get(email=email).is_active:
                raise serializers.ValidationError(
                    detail={
                        "info": "Этот пользователь не подтвердил адрес электронной почты. Пожалуйста, зарегистрируйтесь еще раз."
                    }
                )

        if auth.authenticate(email=email, password=password) is None:
            raise serializers.ValidationError(detail={"info": "Неверный пароль."})
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=50,
        required=True,
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=50,
        required=True,
    )

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]

    def validate(self, attrs):
        email = attrs.get("email", "").lower()
        password1 = attrs.get("password1", "")
        password2 = attrs.get("password2", "")

        if UserSocialAuth.objects.filter(user__email=email).exists():
            raise serializers.ValidationError(
                detail={
                    "info": "Пользователь с этим адресом эл. почты был зарегистрирован с помощью Google/Яндекс. Пожалуйста, войдите в систему, используя тот же метод."
                },
            )

        if password1 != password2:
            raise serializers.ValidationError(
                detail={"info": "Пароли не совпадают."}
            )

        try:
            validate_password(password1)
        except exceptions.ValidationError as e:
            error = [str(error) for error in e.messages][0]
            raise serializers.ValidationError(detail={"info": error})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password1", None)

        instance = self.Meta.model(**validated_data)

        if instance.is_superuser:
            instance.is_active = True
        else:
            instance.is_active = False

        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class SetPasswordSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=50,
        required=True,
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=50,
        required=True,
    )

    class Meta:
        model = User
        fields = ["password1", "password2"]

    def validate(self, attrs):
        password1 = attrs.get("password1", "")
        password2 = attrs.get("password2", "")

        if password1 != password2:
            raise serializers.ValidationError(
                detail={"info": "Пароли не совпадают."}
            )

        try:
            validate_password(password1)
        except exceptions.ValidationError as e:
            error = [str(error) for error in e.messages][0]
            raise serializers.ValidationError(detail={"info": error})

        return attrs
