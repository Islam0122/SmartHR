from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    GoogleAuthAPIView,
    VerifyEmailAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    MeAPIView,
    StudentProfileViewSet,
)

app_name = 'accounts'

router = DefaultRouter()
router.register(r'profile', StudentProfileViewSet, basename='student-profile')

urlpatterns = [
    # ===== Аутентификация =====
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('google/', GoogleAuthAPIView.as_view(), name='google-auth'),

    # ===== Email верификация =====
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),

    # ===== Сброс пароля =====
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

    # ===== JWT токены =====
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # ===== Текущий пользователь =====
    path('me/', MeAPIView.as_view(), name='me'),

    # ===== Router URLs (профиль студента) =====
    path('', include(router.urls)),
]