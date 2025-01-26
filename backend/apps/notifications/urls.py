from .views import NotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = []

urlpatterns += router.urls
