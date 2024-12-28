from .views import CollectionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"collections", CollectionViewSet, basename="collections")

urlpatterns = []

urlpatterns += router.urls
