from django.contrib import auth
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login as login_user, logout as logout_user
from django.core.exceptions import ValidationError as DjangoValidationError


User = get_user_model()


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
        fields = ["pk", "email", "password1", "password2"]
        extra_kwargs = {
            "pk": {"read_only": True},
        }

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError(
                detail={"info": "Password doesn't match."}
            )

        try:
            validate_password(attrs["password1"])
        except DjangoValidationError as e:
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


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ["password", "email"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        if not User.objects.filter(email=email).exists():
            raise AuthenticationFailed(
                {"message": "User with this Email doesn't exists.", "payload": {}}
            )
        if not user.is_active:
            raise AuthenticationFailed(
                {
                    "message": "This user has not verified Email. Please Sign Up again.",
                    "payload": {},
                }
            )
        
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                {"message": "Incorrect Password.", "payload": {}}
            )
        
        login_user(self.context["request"], user)
        return {"message": "OK", "payload": {user.email}}
