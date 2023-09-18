from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint

from .constants import CHARS_MAX_LEN, EMAIL_MAX_LEN

VALIDATE_USERNAME_MSG = (
    'Username может содержать только буквы,'
    ' цифры или следующие символы: @/./+/-/_'
)


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    email = models.EmailField(
        max_length=EMAIL_MAX_LEN,
        blank=False,
        verbose_name='Почта',
        unique=True,
    )
    username = models.CharField(
        max_length=CHARS_MAX_LEN,
        unique=True,
        blank=False,
        verbose_name='Никнейм',
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+$', message=VALIDATE_USERNAME_MSG)
        ],
    )
    first_name = models.CharField(
        max_length=CHARS_MAX_LEN,
        verbose_name='Имя',
        blank=False,
    )
    last_name = models.CharField(
        max_length=CHARS_MAX_LEN,
        verbose_name='Фамилия',
        blank=False,
    )
    password = models.CharField(
        max_length=CHARS_MAX_LEN, verbose_name='Пароль'
    )

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ('id', 'username')

    def __str__(self):
        return self.get_full_name()


class Subscription(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'], name='user_author_unique'
            )
        ]

    def __str__(self):
        return f'Пользователь {self.user} подписался на {self.author}'
