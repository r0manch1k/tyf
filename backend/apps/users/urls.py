from django.urls import path
from .views import *

urlpatterns = [
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("register/", Register.as_view()),
    path("verification/", Verification.as_view()),
    path("set_password/", SetPassword.as_view()),
    path("reset_password/", ResetPassword.as_view()),
]
