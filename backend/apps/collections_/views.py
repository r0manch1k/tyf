from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework.decorators import action
from .serializer import CollectionSerializer
from .models import Collection


class CollectionViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
