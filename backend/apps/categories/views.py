from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import AllowAny

# from rest_framework.decorators import action
from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
