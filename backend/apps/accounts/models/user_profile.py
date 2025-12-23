from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='О себе'
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон'
    )
    linkedin = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='LinkedIn'
    )
    contacts = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Контакты (WhatsApp, Telegram и т.д.)'
    )
    website = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Личный сайт / портфолио'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - Профиль"
