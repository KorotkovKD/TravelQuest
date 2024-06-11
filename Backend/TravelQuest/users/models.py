from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        verbose_name="Почта  пользователя", unique=True, max_length=254
    )
    REQUIRED_FIELDS = ("email", )

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
        return self.value
