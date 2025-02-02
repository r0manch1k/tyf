from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_prometheus.urls")),
    path("api/v1/", include("apps.users.urls")),
    path("api/v1/", include("apps.profiles.urls")),
    path("api/v1/", include("apps.categories.urls")),
    path("api/v1/", include("apps.collections.urls")),
    path("api/v1/", include("apps.posts.urls")),
    path("api/v1/", include("apps.comments.urls")),
    path("api/v1/", include("apps.registry.urls")),
    path("api/v1/", include("apps.notifications.urls")),
    path("api/v1/", include("apps.chats.urls")),
    path("api/v1/", include("apps.tye.urls")),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
