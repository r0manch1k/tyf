from .views import ChatViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"chats", ChatViewSet, basename="chats")

urlpatterns = []

urlpatterns += router.urls
