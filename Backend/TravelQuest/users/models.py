from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):

    email = models.EmailField(
        verbose_name="Почта  пользователя", unique=True, max_length=254
    )
    lvl = models.PositiveSmallIntegerField(
        verbose_name="Уровень пользователя",
        null=True,
        validators=(
            MinValueValidator(1, message="Минимальный уровень: 1"),
        ))
    REQUIRED_FIELDS = ["email", "lvl", ]

    class Meta:
        db_table = "auth_user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        indexes = (models.Index(fields=("email",), name="email_idx"),)
        ordering = ("-id",)

    @property
    def is_authenticated(self):
        return True
