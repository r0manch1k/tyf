from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializer import ItemSerializer


@api_view(["GET"])
def getUsername(request):
    username = User.objects.all()
    serializer = ItemSerializer(username, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def addItem(request):
    return Response("post request")
