from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from drf_spectacular.utils import extend_schema, OpenApiParameter
from ..models import HRProfile
from ..serializers import (
    HRProfileSerializer,
    HRSerializer,
    CreateHRSerializer,
    UpdateHRProfileSerializer,
    HRPasswordSetSerializer,
)
from ..permissions import IsAdmin

User = get_user_model()


class HRViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = HRProfile.objects.select_related('user', 'created_by').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateHRSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateHRProfileSerializer
        elif self.action == 'list':
            return HRSerializer
        return HRProfileSerializer

    @extend_schema(
        summary="Получить список всех HR",
        description="Возвращает список всех HR пользователей с основной информацией"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получить детальную информацию о HR",
        description="Возвращает полную информацию о конкретном HR пользователе"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Создать нового HR пользователя",
        description="Создает нового HR пользователя. Доступно только администраторам. "
                    "HR получит email с инструкциями для установки пароля."
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hr_profile = serializer.save()
            response_serializer = HRProfileSerializer(hr_profile)

            return Response({
                'message': 'HR пользователь успешно создан. Инструкции отправлены на email.',
                'hr': response_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Обновить профиль HR",
        description="Полное обновление профиля HR пользователя"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частично обновить профиль HR",
        description="Частичное обновление профиля HR пользователя"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Удалить HR пользователя",
        description="Удаляет HR пользователя и его профиль. Действие необратимо."
    )
    def destroy(self, request, *args, **kwargs):
        hr_profile = self.get_object()
        user = hr_profile.user

        user.delete()

        return Response({
            'message': 'HR пользователь успешно удален'
        }, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Активировать/деактивировать HR",
        description="Изменяет статус активности HR пользователя"
    )
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        hr_profile = self.get_object()
        user = hr_profile.user

        user.is_active = not user.is_active
        user.save()

        status_text = "активирован" if user.is_active else "деактивирован"

        return Response({
            'message': f'HR пользователь {status_text}',
            'is_active': user.is_active
        })

    @extend_schema(
        summary="Сбросить пароль HR",
        description="Генерирует новый пароль для HR и отправляет его на email"
    )
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        hr_profile = self.get_object()
        user = hr_profile.user

        user.set_random_password_and_notify()

        return Response({
            'message': 'Новый пароль отправлен на email HR пользователя'
        })


class HRMeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Получить профиль текущего HR",
        description="Возвращает профиль авторизованного HR пользователя",
        responses={200: HRProfileSerializer}
    )
    def get(self, request):
        # Проверяем, что пользователь является HR
        if request.user.role != 'hr':
            return Response({
                'error': 'Доступ разрешен только для HR пользователей'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            hr_profile = HRProfile.objects.select_related('user', 'created_by').get(user=request.user)
            serializer = HRProfileSerializer(hr_profile)
            return Response(serializer.data)
        except HRProfile.DoesNotExist:
            return Response({
                'error': 'Профиль HR не найден'
            }, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Обновить профиль текущего HR",
        description="Обновляет профиль авторизованного HR пользователя",
        request=UpdateHRProfileSerializer,
        responses={200: HRProfileSerializer}
    )
    def patch(self, request):
        if request.user.role != 'hr':
            return Response({
                'error': 'Доступ разрешен только для HR пользователей'
            }, status=status.HTTP_403_FORBIDDEN)

        try:
            hr_profile = HRProfile.objects.get(user=request.user)
            serializer = UpdateHRProfileSerializer(
                hr_profile,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                serializer.save()
                response_serializer = HRProfileSerializer(hr_profile)
                return Response({
                    'message': 'Профиль успешно обновлен',
                    'profile': response_serializer.data
                })

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except HRProfile.DoesNotExist:
            return Response({
                'error': 'Профиль HR не найден'
            }, status=status.HTTP_404_NOT_FOUND)


class HRPasswordSetView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Установить пароль для HR",
        description="HR пользователь устанавливает свой пароль по ссылке из email",
        request=HRPasswordSetSerializer,
        responses={
            200: {'description': 'Пароль успешно установлен'},
            400: {'description': 'Неверные данные или токен'}
        }
    )
    def post(self, request):
        serializer = HRPasswordSetSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            uid = serializer.validated_data['uid']
            password = serializer.validated_data['password']

            try:
                # Декодируем user_id
                user_id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=user_id)

                # Проверяем, что пользователь является HR
                if user.role != 'hr':
                    return Response({
                        'error': 'Эта ссылка предназначена только для HR пользователей'
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Проверяем токен
                if default_token_generator.check_token(user, token):
                    # Устанавливаем новый пароль
                    user.set_password(password)
                    user.is_verified = True
                    user.is_active = True
                    user.save()

                    return Response({
                        'message': 'Пароль успешно установлен. Теперь вы можете войти в систему.',
                        'email': user.email
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': 'Неверный или устаревший токен. Запросите новую ссылку у администратора.'
                    }, status=status.HTTP_400_BAD_REQUEST)

            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({
                    'error': 'Неверная ссылка для установки пароля'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HRLoginAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Вход HR в систему",
        description="Аутентификация HR пользователя",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'},
                    'password': {'type': 'string', 'format': 'password'}
                },
                'required': ['email', 'password']
            }
        }
    )
    def post(self, request):
        from django.contrib.auth import authenticate
        from rest_framework_simplejwt.tokens import RefreshToken

        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({
                'error': 'Email и пароль обязательны'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({
                'error': 'Неверный email или пароль'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if user.role != 'hr':
            return Response({
                'error': 'Доступ разрешен только для HR пользователей'
            }, status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            return Response({
                'error': 'Аккаунт деактивирован. Обратитесь к администратору.'
            }, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        try:
            hr_profile = HRProfile.objects.get(user=user)
            profile_data = HRProfileSerializer(hr_profile).data
        except HRProfile.DoesNotExist:
            profile_data = None

        return Response({
            'message': 'Вход выполнен успешно',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
            'profile': profile_data
        }, status=status.HTTP_200_OK)