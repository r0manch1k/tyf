from django.urls import path
from .views import getUsername, addItem

urlpatterns = [
    path('get/', getUsername),
    path('add/', addItem),
]
