from django.db import models
from django.conf import settings

class HRProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='HR пользователь'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='О себе'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_hr_profiles',
        verbose_name='Создано администратором'
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name='Телефон'
    )
    company = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Компания'
    )
    department = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Отдел'
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
        verbose_name='Сайт / портфолио компании'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль HR'
        verbose_name_plural = 'Профили HR'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} - HR"
