from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, UserProfile, HRProfile
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'role', 'is_verified', 'is_active', 'auth_type', 'created_at']
    list_filter = ['role', 'is_verified', 'is_active', 'auth_type', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'first_name', 'last_name', 'password')
        }),
        ('Статусы', {
            'fields': ('is_verified', 'is_allowed', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Роли и типы', {
            'fields': ('role', 'auth_type')
        }),
        ('Права доступа', {
            'fields': ('user_permissions',),
            'classes': ('collapse',)
        }),
        ('Важные даты', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        ('Создание пользователя', {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'last_login']

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = 'ФИО'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user_name', 'get_email', 'phone', 'has_resume', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
    ordering = ['-created_at']

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Контактная информация', {
            'fields': ('phone', 'linkedin', 'contacts', 'website')
        }),
        ('О себе', {
            'fields': ('bio',)
        }),
        ('Документы', {
            'fields': ('resume',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def get_user_name(self, obj):
        return obj.user.full_name

    get_user_name.short_description = 'Пользователь'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

    def has_resume(self, obj):
        if obj.resume:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')

    has_resume.short_description = 'Резюме'


@admin.register(HRProfile)
class HRProfileAdmin(admin.ModelAdmin):
    list_display = ['get_hr_name', 'get_email', 'company', 'department', 'phone',
                    'is_active', 'created_by_name', 'created_at']
    list_filter = ['company', 'department', 'created_at', 'user__is_active']
    search_fields = ['user__email', 'user__first_name', 'user__last_name',
                     'company', 'department', 'phone']
    ordering = ['-created_at']

    fieldsets = (
        ('HR Пользователь', {
            'fields': ('user', 'created_by')
        }),
        ('Компания', {
            'fields': ('company', 'department')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'contacts', 'linkedin', 'website')
        }),
        ('О себе', {
            'fields': ('bio',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at', 'created_by']

    def get_hr_name(self, obj):
        return obj.user.full_name

    get_hr_name.short_description = 'HR'

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = 'Email'

    def is_active(self, obj):
        if obj.user.is_active:
            return format_html('<span style="color: green;">✓ Активен</span>')
        return format_html('<span style="color: red;">✗ Неактивен</span>')

    is_active.short_description = 'Статус'

    def created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.full_name
        return '-'

    created_by_name.short_description = 'Создал'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.site_header = "SmartHR Администрирование"
admin.site.site_title = "SmartHR Admin"
admin.site.index_title = "Добро пожаловать в панель администрирования SmartHR"