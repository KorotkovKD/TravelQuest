from django.contrib.auth.hashers import check_password
from django.shortcuts import render, get_object_or_404
from rest_framework import filters, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import (PasswordSerializer,
                          LoginSerializer,
                          MatchesSerializer,
                          MatchesAnswersSerializer,
                          UserSerializer,
                          UserRegistrationSerializer, )
from .mixins import MatchesMixinSet
from users.models import User, Wallet
from users.views import activate_email
from quests.models import Matches


@api_view(("POST", ))
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get("email")
    user = get_object_or_404(User, email=email)
    password = serializer.data.get("password")
    if not user.is_confirmed:
        return activate_email(request, user, email)
    if not user.is_active:
        return Response({"detail": "Пользователь заблокирован."},
                        status=status.HTTP_403_FORBIDDEN)
    if check_password(password, user.password):
        token = Token.objects.create(user=user)
        return Response({"token": str(token.key)}, status=status.HTTP_200_OK)
    return Response({"detail": "Неверный пароль."},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(("POST", ))
def registration(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    if User.objects.filter(email=email).exists():
        return Response({"detail": "Почта уже используется."},
                        status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    Wallet.objects.create(owner=user, value=0)
    return activate_email(request, user, email)


@api_view(("DELETE", ))
@permission_classes((IsAuthenticated,))
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("PATCH", ))
@permission_classes((IsAuthenticated,))
def change_password(request):
    serializer = PasswordSerializer(data=request.data,
                                    context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Пaроль изменён."},
                    status=status.HTTP_200_OK)


@api_view(("GET", "PATCH", ))
@permission_classes((IsAuthenticated,))
def profile(request):
    instance = request.user
    if request.method == 'GET':
        serializer = UserSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    serializer = UserSerializer(instance, data=request.data, partial=True, )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Профиль изменён."},
                    status=status.HTTP_200_OK)


class MatchesViewSet(MatchesMixinSet):
    serializer_class = MatchesSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, )
    http_method_names = ("get", "patch", "post", )
    queryset = Matches.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == "PATCH":
            serializer_class = MatchesAnswersSerializer
        else:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                          context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
