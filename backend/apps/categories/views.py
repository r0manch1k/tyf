from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
