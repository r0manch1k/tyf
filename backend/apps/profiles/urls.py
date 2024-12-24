from django.urls import path
from .views import *

urlpatterns = [
    path("all/", AllProfiles),
    path("<str:username>/", ProfileByUsername),
    # path('add/', addItem),
]
