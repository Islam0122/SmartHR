# SmartHR Authentication API Documentation

## Обзор системы ролей

### Роли пользователей:
1. **Admin** - суперпользователь с полным доступом
2. **HR** - HR-менеджер, управляет вакансиями и кандидатами
3. **User** - обычный пользователь (кандидат)

---

## 🔐 Endpoints для обычных пользователей (Кандидаты)

### 1. Регистрация
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "candidate@example.com",
  "first_name": "Иван",
  "last_name": "Иванов",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

**Ответ:**
```json
{
  "message": "Регистрация успешна. Проверьте email для подтверждения.",
  "user": {
    "id": 1,
    "email": "candidate@example.com",
    "first_name": "Иван",
    "last_name": "Иванов",
    "full_name": "Иван Иванов",
    "role": "user",
    "is_verified": false,
    "is_active": true,
    "auth_type": "local",
    "created_at": "2025-01-15T10:30:00Z"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Вход в систему
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "candidate@example.com",
  "password": "SecurePassword123!"
}
```

### 3. Вход через Google
```http
POST /api/auth/google/
Content-Type: application/json

{
  "token": "google_id_token_here"
}
```

### 4. Подтверждение email
```http
GET /api/auth/verify-email/?token={token}&uid={uid}
```

### 5. Получить текущего пользователя
```http
GET /api/auth/me/
Authorization: Bearer {access_token}
```

### 6. Управление профилем
```http
GET /api/auth/profile/
Authorization: Bearer {access_token}

PATCH /api/auth/profile/{id}/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

{
  "bio": "О себе",
  "phone": "+996555123456",
  "linkedin": "https://linkedin.com/in/ivanov",
  "resume": <file>
}
```

---

## 👔 Endpoints для HR пользователей

### 1. Вход HR в систему
```http
POST /api/auth/hr/login/
Content-Type: application/json

{
  "email": "hr@company.com",
  "password": "HRPassword123!"
}
```

**Ответ:**
```json
{
  "message": "Вход выполнен успешно",
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  },
  "user": {
    "id": 2,
    "email": "hr@company.com",
    "first_name": "Мария",
    "last_name": "Петрова",
    "role": "hr"
  },
  "profile": {
    "id": 1,
    "company": "Tech Company",
    "department": "HR Department",
    "phone": "+996555999888"
  }
}
```

### 2. Установка пароля HR (первый вход)
```http
POST /api/auth/hr/set-password/
Content-Type: application/json

{
  "token": "token_from_email",
  "uid": "uid_from_email",
  "password": "NewSecurePassword123!",
  "password_confirm": "NewSecurePassword123!"
}
```

### 3. Получить профиль текущего HR
```http
GET /api/auth/hr/me/
Authorization: Bearer {access_token}
```

**Ответ:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "email": "hr@company.com",
    "first_name": "Мария",
    "last_name": "Петрова",
    "is_verified": true,
    "is_active": true,
    "role": "hr",
    "created_at": "2025-01-10T09:00:00Z"
  },
  "user_email": "hr@company.com",
  "user_full_name": "Мария Петрова",
  "bio": "HR менеджер с 5-летним опытом",
  "phone": "+996555999888",
  "company": "Tech Company",
  "department": "HR Department",
  "linkedin": "https://linkedin.com/in/petrova",
  "contacts": "Telegram: @petrova_hr",
  "website": "https://techcompany.com",
  "created_by": 1,
  "created_by_name": "Admin User",
  "created_at": "2025-01-10T09:00:00Z",
  "updated_at": "2025-01-15T14:30:00Z"
}
```

### 4. Обновить профиль HR
```http
PATCH /api/auth/hr/me/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "first_name": "Мария",
  "last_name": "Петрова-Сидорова",
  "bio": "Обновленная информация обо мне",
  "phone": "+996555999777",
  "contacts": "Telegram: @petrova_hr, WhatsApp: +996555999777"
}
```

---

## 👨‍💼 Endpoints для Admin (управление HR)

### 1. Получить список всех HR
```http
GET /api/auth/hr/
Authorization: Bearer {access_token}
```

**Ответ:**
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "user_full_name": "Мария Петрова",
      "user_email": "hr@company.com",
      "company_name": "Tech Company",
      "department": "HR Department",
      "phone": "+996555999888",
      "created_at": "2025-01-10T09:00:00Z"
    }
  ]
}
```

### 2. Получить детальную информацию о HR
```http
GET /api/auth/hr/{id}/
Authorization: Bearer {access_token}
```

### 3. Создать нового HR
```http
POST /api/auth/hr/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "email": "new.hr@company.com",
  "first_name": "Алексей",
  "last_name": "Сидоров",
  "company": "Tech Company",
  "department": "Recruitment",
  "phone": "+996555888777",
  "bio": "Специалист по подбору персонала",
  "linkedin": "https://linkedin.com/in/sidorov",
  "contacts": "Telegram: @sidorov_hr",
  "website": "https://techcompany.com"
}
```

**Ответ:**
```json
{
  "message": "HR пользователь успешно создан. Инструкции отправлены на email.",
  "hr": {
    "id": 2,
    "user": {
      "id": 5,
      "email": "new.hr@company.com",
      "first_name": "Алексей",
      "last_name": "Сидоров",
      "is_verified": false,
      "is_active": true,
      "role": "hr"
    },
    "company": "Tech Company",
    "department": "Recruitment"
  }
}
```

### 4. Обновить HR профиль
```http
PATCH /api/auth/hr/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "department": "Senior Recruitment",
  "bio": "Обновленная биография"
}
```

### 5. Удалить HR
```http
DELETE /api/auth/hr/{id}/
Authorization: Bearer {access_token}
```

### 6. Активировать/деактивировать HR
```http
POST /api/auth/hr/{id}/toggle_active/
Authorization: Bearer {access_token}
```

**Ответ:**
```json
{
  "message": "HR пользователь деактивирован",
  "is_active": false
}
```

### 7. Сбросить пароль HR
```http
POST /api/auth/hr/{id}/reset_password/
Authorization: Bearer {access_token}
```

**Ответ:**
```json
{
  "message": "Новый пароль отправлен на email HR пользователя"
}
```

---

## 🔄 Общие endpoints

### 1. Обновить токен
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Выход из системы
```http
POST /api/auth/logout/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Запрос на сброс пароля
```http
POST /api/auth/password-reset/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### 4. Подтверждение сброса пароля
```http
POST /api/auth/password-reset-confirm/
Content-Type: application/json

{
  "token": "token_from_email",
  "uid": "uid_from_email",
  "password": "NewPassword123!",
  "password_confirm": "NewPassword123!"
}
```

---

## 📧 Email уведомления

### 1. Приглашение HR
**Тема:** Добро пожаловать в SmartHR

**Содержание:**
```
Привет, {first_name}! 👋

Мы рады приветствовать вас в системе SmartHR! 🎉

Ваши данные для входа:
• Логин: {email}
• Пароль: {password}

⚠️ Не передавайте эти данные третьим лицам!

Если возникнут вопросы, мы всегда на связи. 🤝

С уважением,
Команда SmartHR 🚀
```

### 2. Подтверждение email (для кандидатов)
**Тема:** Подтверждение email - SmartHR

**Содержание:**
```
Здравствуйте, {first_name}!

Спасибо за регистрацию в SmartHR!

Пожалуйста, подтвердите ваш email, перейдя по ссылке:
{verification_link}

Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.

С уважением,
Команда SmartHR
```

---

## 🔒 Безопасность

### Требования к паролям:
- Минимум 8 символов
- Должен содержать буквы и цифры
- Рекомендуется использовать спецсимволы

### JWT токены:
- **Access token**: действителен 1 час
- **Refresh token**: действителен 7 дней
- При обновлении refresh токена старый добавляется в blacklist

### Разграничение доступа:
- **Admin**: полный доступ ко всем функциям
- **HR**: управление вакансиями и кандидатами
- **User**: просмотр вакансий, прохождение тестов, управление своим профилем

---

## 📊 Коды ответов

| Код | Значение |
|-----|----------|
| 200 | Успешный запрос |
| 201 | Ресурс создан |
| 204 | Успешно, нет содержимого |
| 400 | Ошибка валидации |
| 401 | Не авторизован |
| 403 | Доступ запрещен |
| 404 | Ресурс не найден |
| 500 | Внутренняя ошибка сервера |

---

## 🧪 Тестирование API

### Swagger UI:
```
http://localhost:8000/api/swagger/
```

### ReDoc:
```
http://localhost:8000/api/redoc/
```

### OpenAPI Schema:
```
http://localhost:8000/api/schema/
```

---

## 🚀 Быстрый старт

### 1. Создать суперпользователя (Admin)
```bash
python manage.py createsuperuser
```

### 2. Зайти в Django Admin
```
http://localhost:8000/admin/
```

### 3. Создать HR пользователя через API
```bash
curl -X POST http://localhost:8000/api/auth/hr/ \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "hr@company.com",
    "first_name": "Мария",
    "last_name": "Петрова",
    "company": "Tech Company"
  }'
```

### 4. HR получит email и установит пароль через:
```
POST /api/auth/hr/set-password/
```

### 5. HR может войти через:
```
POST /api/auth/hr/login/
```

---
