from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с указанными данными.
        """
        if not email:
            raise ValueError("Email обязателен")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_hr_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Создает и сохраняет HR пользователя.
        HR автоматически получает is_staff=True, is_active=True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "hr")  # Роль HR

        return self.create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с полными правами.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")  # Роль админ

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)
