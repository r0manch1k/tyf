from django.urls import path
from .views import *

urlpatterns = [
    path("overview/", apiOverview),
    path("login/", Login.as_view()),
    path("register/", Register.as_view()),
    path("verify-otp/", VerifyOTP.as_view()),
    path("resend-otp/", ResendOTP.as_view()),
]
