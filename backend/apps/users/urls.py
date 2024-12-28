from django.urls import path
from .views import *

urlpatterns = [
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("register/", Register.as_view()),
    path("verification/", Verification.as_view()),
]
