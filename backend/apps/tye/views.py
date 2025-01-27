from pymongo import MongoClient
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

MAX_RECORDS = 10

class LeaderBoard(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        client = MongoClient(settings.TYE_MONGO_URL)
        db = client["highscores"]
        collection = db["players"]

        try:
            users = list(
                collection.find({}, {"_id": 0, "username": 1, "highScore": 1})
                .sort([("highScore", -1), ("username", 1)])
                .limit(MAX_RECORDS)
            )

            return Response(users, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error fetching scores: {e}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
