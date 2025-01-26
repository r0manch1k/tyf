from .views import TagsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"tags", TagsViewSet, basename="tags")

urlpatterns = []

urlpatterns += router.urls
