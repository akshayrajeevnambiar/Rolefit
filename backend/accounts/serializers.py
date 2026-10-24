"""Input checks for register and login.

The password is write-only. It is never part of a response.
"""

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from accounts.models import User

# Long passwords are hashed on purpose. A huge one is just a CPU sink.
PASSWORD_MAX_LENGTH = 128


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        trim_whitespace=False,
        write_only=True,
    )

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "An account with this email already exists."}
            )
        try:
            validate_password(attrs["password"], user=User(email=attrs["email"]))
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)}) from exc
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        trim_whitespace=False,
        write_only=True,
    )

    def validate_email(self, value: str) -> str:
        return value.strip().lower()
