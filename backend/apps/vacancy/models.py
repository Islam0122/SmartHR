from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Specialization(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='specializations'
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'
        unique_together = ('category', 'name')
        ordering = ['name']

    def __str__(self):
        return f'{self.category.name} — {self.name}'


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['name']

    def __str__(self):
        return self.name


class Vacancy(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликована'
        CLOSED = 'closed', 'Закрыта'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'full_time', 'Полная занятость'
        PART_TIME = 'part_time', 'Частичная занятость'
        CONTRACT = 'contract', 'Контракт'
        INTERNSHIP = 'internship', 'Стажировка'

    class WorkFormat(models.TextChoices):
        ONSITE = 'onsite', 'Офис'
        REMOTE = 'remote', 'Удалённо'
        HYBRID = 'hybrid', 'Гибрид'

    class ExperienceLevel(models.TextChoices):
        JUNIOR = 'junior', 'Junior'
        MIDDLE = 'middle', 'Middle'
        SENIOR = 'senior', 'Senior'
        LEAD = 'lead', 'Lead'
        ANY = 'any', 'Не важно'

    hr = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='HR'
    )

    company_name = models.CharField(max_length=255, verbose_name='Компания')
    title = models.CharField(max_length=255)
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='vacancies'
    )

    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='vacancies'
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices
    )

    work_format = models.CharField(
        max_length=20,
        choices=WorkFormat.choices
    )

    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ANY
    )

    location = models.CharField(max_length=255, blank=True)
    salary_from = models.IntegerField(null=True, blank=True)
    salary_to = models.IntegerField(null=True, blank=True)
    salary_currency = models.CharField(max_length=10, default='USD')
    salary_is_hidden = models.BooleanField(default=False)

    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='vacancies'
    )

    ai_weight_config = models.JSONField(default=dict, blank=True)
    min_ai_score = models.FloatField(default=0)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['specialization']),
            models.Index(fields=['experience_level']),
            models.Index(fields=['company_name']),
        ]


    def __str__(self):
        return f'{self.title} — {self.company_name}'

