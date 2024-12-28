from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializer import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, slug=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
