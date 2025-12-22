from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    verification_link = (
        f"{request.scheme}://{request.get_host()}"
        f"/api/auth/verify-email/?token={token}&uid={uid}"
    )

    subject = 'Подтверждение email -  SmartHR'
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


def send_welcome_email(self, password):
        if not self.email:
            return

        subject = 'Добро пожаловать в SmartHR'

        html_message = f'''
        <h2>Привет, {self.username}! 👋</h2>

        <p>Мы рады приветствовать вас в системе <b>SmartHR</b>! 🎉</p>

        <p><b>Ваши данные для входа:</b></p>
        <ul>
            <li><b>Логин:</b> {self.username}</li>
            <li><b>Пароль:</b> {password}</li>
        </ul>

        <p style="color: red;"><b>⚠️ Не передавайте эти данные третьим лицам!</b></p>

        <p>Если возникнут вопросы, мы всегда на связи. 🤝</p>

        <p>С уважением,<br>
        Duishobaev Islam (<a href="mailto:duishobaevislam01@gmail.com">duishobaevislam01@gmail.com</a>) 🚀</p>
        '''

        plain_message = strip_tags(html_message)  # Удаляем HTML теги для обычной версии

        send_mail(
            subject=subject,
            message=plain_message,  # Обычная версия
            from_email='duishobaevislam01@gmail.com',
            recipient_list=[self.email],
            html_message=html_message  # HTML-версия
        )

