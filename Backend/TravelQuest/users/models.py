from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import CustomUserManager


class User(AbstractUser):

    email = models.EmailField(
        verbose_name="Почта  пользователя",
        unique=True,
        max_length=256
    )
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    photo = models.ImageField(
        verbose_name="Фото пользователя",
        blank=True,
        null=True,
        upload_to="users/images/",
    )

    bio = models.TextField(
        verbose_name="Биография пользователя",
        blank=True,
        null=True,
    )

    is_confirmed = models.BooleanField(
        default=False,
        help_text="Почта подтверждена",
        blank=True,
        null=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = (
            models.Index(fields=("email",), name="email_idx"),
        )
        ordering = ("-id",)

    @property
    def is_authenticated(self):
        return True


class Wallet(models.Model):

    owner = models.OneToOneField(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name="Хозяин кошелька",
        related_name='owned_by'
    )
    value = models.PositiveIntegerField(
        verbose_name="Количество Валюты",
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = 'Кошелёк'
        verbose_name_plural = 'Кошельки'
        indexes = (
            models.Index(fields=('owner', ), name='owner_idx'),
        )
        ordering = ('-id', )

    def __str__(self) -> str:
        return str(self.value)
