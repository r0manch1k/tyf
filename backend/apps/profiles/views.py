from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProfileSerializer
from .models import Profile


@api_view(["GET"])
def AllProfiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def ProfileByUsername(request, username):
    profile = Profile.objects.get(username=username)
    serializer = ProfileSerializer(profile, many=False)
    return Response(serializer.data)


# @api_view(["POST"])
# def createProfile(request):
#     serializer = ItemSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)
