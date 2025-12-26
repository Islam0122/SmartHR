from django.contrib import admin
from .models import Category, Specialization, Skill, Vacancy


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company_name',
        'category',
        'specialization',
        'employment_type',
        'work_format',
        'experience_level',
        'status',
        'created_at',
    )
    search_fields = (
        'title',
        'company_name',
        'category__name',
        'specialization__name',
        'skills__name',
    )
    list_filter = (
        'status',
        'category',
        'specialization',
        'employment_type',
        'work_format',
        'experience_level',
        'created_at',
    )
    filter_horizontal = ('skills',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'company_name', 'description', 'responsibilities', 'requirements')
        }),
        ('Категория и специализация', {
            'fields': ('category', 'specialization')
        }),
        ('Условия работы', {
            'fields': ('employment_type', 'work_format', 'experience_level', 'location')
        }),
        ('Зарплата', {
            'fields': ('salary_from', 'salary_to', 'salary_currency', 'salary_is_hidden')
        }),
        ('Навыки и AI', {
            'fields': ('skills', 'ai_weight_config', 'min_ai_score')
        }),
        ('Статус и даты', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
