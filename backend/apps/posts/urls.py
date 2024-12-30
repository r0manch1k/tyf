from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

urlpatterns = []

urlpatterns += router.urls
