from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CollectionSerializer
from .models import Collection


class CollectionViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
