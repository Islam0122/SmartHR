from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.html import strip_tags


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = (
        f"{request.scheme}://{request.get_host()}"
        f"/api/auth/verify-email/?token={token}&uid={uid}"
    )

    subject = 'Подтверждение email - SmartHR'
    message = f'''
Здравствуйте, {user.first_name}!

Спасибо за регистрацию в SmartHR!

Пожалуйста, подтвердите ваш email, перейдя по ссылке:
{verification_link}

Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.

С уважением,
Команда SmartHR
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def send_password_reset_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_link = (
        f"{request.scheme}://{request.get_host()}"
        f"/api/auth/password-reset-confirm/?token={token}&uid={uid}"
    )

    subject = 'Сброс пароля - SmartHR'
    message = f'''
Здравствуйте, {user.first_name}!

Вы запросили сброс пароля для вашего аккаунта в SmartHR.

Перейдите по ссылке для создания нового пароля:
{reset_link}

Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.
Ваш пароль останется без изменений.

С уважением,
Команда SmartHR
    '''

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )


def send_welcome_email(user, password):
    if not user.email:
        return

    subject = 'Добро пожаловать в SmartHR'

    html_message = f'''
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #4CAF50;">Привет, {user.first_name}! 👋</h2>

            <p>Мы рады приветствовать вас в системе <strong>SmartHR</strong>! 🎉</p>

            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0; color: #333;">Ваши данные для входа:</h3>
                <p style="margin: 10px 0;">
                    <strong>Email:</strong> {user.email}<br>
                    <strong>Временный пароль:</strong> <code style="background-color: #fff; padding: 5px 10px; border-radius: 3px;">{password}</code>
                </p>
            </div>

            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                <p style="margin: 0; color: #856404;">
                    <strong>⚠️ Важно:</strong> Рекомендуем изменить пароль после первого входа в систему.
                    Не передавайте эти данные третьим лицам!
                </p>
            </div>

            <div style="margin: 30px 0; text-align: center;">
                <p style="margin-bottom: 20px;">Вы можете войти в систему по адресу:</p>
                <a href="{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}" 
                   style="display: inline-block; padding: 12px 30px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">
                    Войти в систему
                </a>
            </div>

            <p>Если возникнут вопросы, мы всегда на связи. 🤝</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

            <p style="color: #666; font-size: 14px;">
                С уважением,<br>
                Команда SmartHR 🚀<br>
                <a href="mailto:support@smarthr.com" style="color: #4CAF50;">support@smarthr.com</a>
            </p>
        </div>
    </body>
    </html>
    '''

    # Создаём простую текстовую версию
    plain_message = f'''
Привет, {user.first_name}!

Мы рады приветствовать вас в системе SmartHR!

Ваши данные для входа:
• Email: {user.email}
• Временный пароль: {password}

⚠️ Важно: Рекомендуем изменить пароль после первого входа в систему.
Не передавайте эти данные третьим лицам!

Если возникнут вопросы, мы всегда на связи.

С уважением,
Команда SmartHR
support@smarthr.com
    '''

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки приветственного письма: {e}")
        return False


def send_hr_password_set_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    base_url = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'
    set_password_link = f"{base_url}/api/auth/hr/set-password/?token={token}&uid={uid}"

    subject = 'Установите пароль для доступа в SmartHR'

    html_message = f'''
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #4CAF50;">Добро пожаловать в SmartHR, {user.first_name}! 👋</h2>

            <p>Вы были добавлены в систему SmartHR в качестве HR-менеджера.</p>

            <p>Для начала работы необходимо установить пароль для вашего аккаунта.</p>

            <div style="background-color: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 10px 0;">
                    <strong>Ваш email:</strong> {user.email}
                </p>
            </div>

            <div style="margin: 30px 0; text-align: center;">
                <a href="{set_password_link}" 
                   style="display: inline-block; padding: 12px 30px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;">
                    Установить пароль
                </a>
            </div>

            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                <p style="margin: 0; color: #856404;">
                    <strong>⚠️ Внимание:</strong> Ссылка действительна в течение 24 часов.
                    Если срок истёк, обратитесь к администратору для получения новой ссылки.
                </p>
            </div>

            <p>Если вы не запрашивали создание аккаунта, просто проигнорируйте это письмо.</p>

            <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">

            <p style="color: #666; font-size: 14px;">
                С уважением,<br>
                Команда SmartHR 🚀<br>
                <a href="mailto:support@smarthr.com" style="color: #4CAF50;">support@smarthr.com</a>
            </p>
        </div>
    </body>
    </html>
    '''

    plain_message = f'''
Добро пожаловать в SmartHR, {user.first_name}!

Вы были добавлены в систему SmartHR в качестве HR-менеджера.

Для начала работы необходимо установить пароль для вашего аккаунта.

Ваш email: {user.email}

Перейдите по ссылке для установки пароля:
{set_password_link}

⚠️ Внимание: Ссылка действительна в течение 24 часов.

Если вы не запрашивали создание аккаунта, просто проигнорируйте это письмо.

С уважением,
Команда SmartHR
support@smarthr.com
    '''

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Ошибка отправки письма для установки пароля: {e}")
        return False