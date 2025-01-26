from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

# from rest_framework.decorators import action
from .serializers import CollectionSerializer
from .models import Collection


class CollectionViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
