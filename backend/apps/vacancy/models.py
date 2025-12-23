from django.db import models


class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликована'),
        ('closed', 'Закрыта'),
    ]

    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', 'Полная занятость'),
        ('part_time', 'Частичная занятость'),
        ('contract', 'Контракт'),
        ('internship', 'Стажировка'),
    ]

    WORK_FORMAT_CHOICES = [
        ('onsite', 'Офис'),
        ('remote', 'Удалённо'),
        ('hybrid', 'Гибрид'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('junior', 'Junior'),
        ('middle', 'Middle'),
        ('senior', 'Senior'),
        ('lead', 'Lead'),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name='Название вакансии'
    )
    description = models.TextField(
        verbose_name='Описание вакансии'
    )
    requirements = models.TextField(
        verbose_name='Требования'
    )
    responsibilities = models.TextField(
        verbose_name='Обязанности'
    )

    company = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Компания'
    )
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_vacancies',
        verbose_name='Создал (HR)'
    )

    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPE_CHOICES,
        blank=True,
        verbose_name='Тип занятости'
    )
    work_format = models.CharField(
        max_length=50,
        choices=WORK_FORMAT_CHOICES,
        blank=True,
        verbose_name='Формат работы'
    )
    experience_level = models.CharField(
        max_length=50,
        choices=EXPERIENCE_LEVEL_CHOICES,
        blank=True,
        verbose_name='Уровень опыта'
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Локация'
    )
    salary_from = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата от'
    )
    salary_to = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Зарплата до'
    )
    salary_currency = models.CharField(
        max_length=10,
        default='USD',
        verbose_name='Валюта'
    )

    skills = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Навыки'
    )
    ai_weight_config = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='AI веса навыков'
    )
    min_ai_score = models.FloatField(
        default=0,
        verbose_name='Минимальный AI-балл'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус вакансии'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['company']),
            models.Index(fields=['experience_level']),
        ]

    def __str__(self):
        return f'{self.title} — {self.company}'
