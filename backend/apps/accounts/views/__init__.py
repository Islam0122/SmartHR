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
from .user_views import (
    UserProfileViewSet
)
from .hr_views import (
    HRViewSet,
    HRMeAPIView,
    HRPasswordSetView,
    HRLoginAPIView,
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

    #User
    'UserProfileViewSet',

    # HR
    'HRViewSet',
    'HRMeAPIView',
    'HRPasswordSetView',
    'HRLoginAPIView',
]