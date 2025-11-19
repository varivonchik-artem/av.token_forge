from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        )

        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {
                    "password_confirm": "Passwords do not match",
                },
                code="password_mismatch",
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        request = self.context.get("request")

        if request is None:
            raise serializers.ValidationError(
                {"detail": "Request must be provided in serializer context."},
                code="missing_request",
            )

        user = authenticate(
            request=request,
            username=email,
            password=password,
        )

        if user is None:
            raise serializers.ValidationError(
                {"user": "Invalid credentials."},
                code="invalid_credentials",
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "User account is disabled."},
                code="inactive_account",
            )

        attrs["user"] = user
        return attrs

    def create(self, validated_data):
        raise NotImplementedError("UserLoginSerializer does not support create().")

    def update(self, instance, validated_data):
        raise NotImplementedError("UserLoginSerializer does not support update().")
