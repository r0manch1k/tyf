from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializer import ProfileSerializer
from .models import Profile
from django.db.models import Count


class ProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # TODO: recent_users or recent_profiles?
    @action(detail=False, methods=["GET"], url_path="recent", url_name="recent")
    def recent_users(self, request):
        queryset = Profile.objects.all().order_by("-date_joined")[:5]
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False, methods=["GET"], url_path="most-active", url_name="most-active"
    )
    def most_active_users(self, request):
        queryset = Profile.objects.annotate(nposts=Count("posts")).order_by("-nposts")[
            :5
        ]
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
