from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.decorators import action
from .serializer import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
