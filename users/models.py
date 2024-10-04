from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="Почта", unique=True)
    tg_chat_id = models.CharField(verbose_name="Телеграм chat_id", unique=True, max_length=20)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name = "Пользователи"
        ordering = ["-id"]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
