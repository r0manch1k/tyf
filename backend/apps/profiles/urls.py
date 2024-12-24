from django.urls import path
from .views import getAllProfiles, getProfileByUsername

urlpatterns = [
    path('profiles/all', getAllProfiles),
    path('profiles/<str:username>/', getProfileByUsername),
    # path('add/', addItem),
]
