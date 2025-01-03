from .views import CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="categories")

urlpatterns = []

urlpatterns += router.urls
