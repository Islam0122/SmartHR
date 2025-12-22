from .auth_views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    GoogleAuthAPIView,
    VerifyEmailAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    MeAPIView,
)
from .student_views import (
    StudentProfileViewSet,
)

__all__ = [
    # Auth
    'RegisterAPIView',
    'LoginAPIView',
    'LogoutAPIView',
    'GoogleAuthAPIView',
    'VerifyEmailAPIView',
    'PasswordResetRequestAPIView',
    'PasswordResetConfirmAPIView',
    'MeAPIView',

    # Student Profile
    'StudentProfileViewSet',
]