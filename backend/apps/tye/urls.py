from django.urls import path
from .views import (
    LeaderBoard,
)

urlpatterns = [
    path("tye/leaderboard/", LeaderBoard.as_view()),
]
