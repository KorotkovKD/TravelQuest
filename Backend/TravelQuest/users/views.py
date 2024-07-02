from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .mail import MAIL_SUBJECT_ACTIVASION, create_activation_link
from .models import User
from .tokens import account_activation_token


def activate_email(request, user, to_email):
    mail_subject = MAIL_SUBJECT_ACTIVASION
    message = create_activation_link(request, user)
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        return Response({"detail": f'Уважаемый {user}, для подтверждения вашего '
                                   'аккаунта пройдите по ссылке на вашей почте.'},
                        status=status.HTTP_200_OK)
    return Response({"detail": "Не удалось отправить mail"},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(('POST',))
def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=uid)
    if account_activation_token.check_token(user, token):
        user.is_confirmed = True
        user.save()
        return Response({"detail": 'Почта подтверждена'},
                        status=status.HTTP_201_CREATED)
    return Response({"detail": "Ссылка недействительна"},
                    status=status.HTTP_400_BAD_REQUEST)
