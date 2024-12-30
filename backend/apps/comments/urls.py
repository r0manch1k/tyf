from .views import CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = []

urlpatterns += router.urls
