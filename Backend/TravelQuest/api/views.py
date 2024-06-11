from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .serializers import LoginSerializer
from users.models import User


@api_view(("POST", ))
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get("email")
    user = get_object_or_404(User, email=email)
    password = serializer.data.get("password")
    if check_password(password, user.password):
        token = Token.objects.create(user=user)
        return Response({"token": str(token.key)}, status=status.HTTP_200_OK)
    return Response({"detail": "Неверный пароль"},
                    status=status.HTTP_400_BAD_REQUEST)
