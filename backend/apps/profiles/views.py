from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ItemSerializer
from .models import Profile


@api_view(["GET"])
def getAllProfiles(request):
    profiles = Profile.objects.all()
    serializer = ItemSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProfileByUsername(request, username):
    profile = Profile.objects.get(username=username)
    serializer = ItemSerializer(profile, many=False)
    return Response(serializer.data)


# @api_view(["POST"])
# def createProfile(request):
#     serializer = ItemSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
