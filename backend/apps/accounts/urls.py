from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    # Auth views
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    GoogleAuthAPIView,
    VerifyEmailAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    MeAPIView,

    # User profile views
    UserProfileViewSet,

    # HR views
    HRViewSet,
    HRMeAPIView,
    HRPasswordSetView,
    HRLoginAPIView,
)

app_name = 'accounts'

# Router для ViewSets
router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')
router.register(r'hr', HRViewSet, basename='hr')

urlpatterns = [
    # ===== Аутентификация обычных пользователей =====
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

    # ===== HR специфичные эндпоинты =====
    path('hr/login/', HRLoginAPIView.as_view(), name='hr-login'),
    path('hr/me/', HRMeAPIView.as_view(), name='hr-me'),
    path('hr/set-password/', HRPasswordSetView.as_view(), name='hr-set-password'),

    # ===== Router URLs =====
    path('', include(router.urls)),
]