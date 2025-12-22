from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..utils.email import send_welcome_email
from ..managers.user_manager import UserManager


class AuthType(models.TextChoices):
    LOCAL = 'local', 'Локальная'
    GOOGLE = 'google', 'Google'


class Role(models.TextChoices):
    ADMIN = 'admin', 'Администратор'
    USER = 'user', 'Пользователь'
    HR = 'hr', 'HR'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email адрес')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    is_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
    is_allowed = models.BooleanField(default=True, verbose_name='Разрешен')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    auth_type = models.CharField(
        max_length=10,
        choices=AuthType.choices,
        default=AuthType.LOCAL,
        verbose_name='Тип аутентификации'
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль пользователя'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def set_random_password_and_notify(self):
        if self.role == Role.HR:
            password = get_random_string(10)
            self.set_password(password)
            self.save()
            send_welcome_email(self, password)
