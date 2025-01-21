from .views import UniversityViewSet, MajorViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"universities", UniversityViewSet, basename="universities")
router.register(r"majors", MajorViewSet, basename="majors")

urlpatterns = []

urlpatterns += router.urls
