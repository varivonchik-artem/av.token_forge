from typing import cast

from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.serializers import UserLoginSerializer, UserRegistrationSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = cast(User, serializer.save())

        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": UserRegistrationSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "You have successfully registered",
            },
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        validated_data = cast(dict, serializer.validated_data)

        user: User = validated_data["user"]

        login(request, user)
        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": UserRegistrationSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "message": "You have successfully logged in",
            },
        }

        return Response(response_data, status=status.HTTP_200_OK)
