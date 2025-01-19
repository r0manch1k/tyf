from django.urls import path
from .views import (
    Login,
    SocialLogin,
    Logout,
    Register,
    Verification,
    SetPassword,
    ResetPassword,
)

urlpatterns = [
    path("users/login/", Login.as_view()),
    path("users/logout/", Logout.as_view()),
    path("users/register/", Register.as_view()),
    path("users/verification/", Verification.as_view()),
    path("users/set_password/", SetPassword.as_view()),
    path("users/reset_password/", ResetPassword.as_view()),
    path("users/login/<str:social>/", SocialLogin.as_view()),
]
