from rest_framework.response import Response
from rest_framework import viewsets
from .models import University, Major
from .serializer import UniversityListSerializer, MajorListSerializer


class UniversityViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = University.objects.all()
        serializer = UniversityListSerializer(queryset, many=True)
        return Response(serializer.data)


class MajorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Major.objects.all()
        serializer = MajorListSerializer(queryset, many=True)
        return Response(serializer.data)
