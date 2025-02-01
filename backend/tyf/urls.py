from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

api_url_prefix = "v1/" if not settings.DEBUG else "api/v1/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("django_prometheus.urls")),
    path(api_url_prefix, include("apps.users.urls")),
    path(api_url_prefix, include("apps.profiles.urls")),
    path(api_url_prefix, include("apps.categories.urls")),
    path(api_url_prefix, include("apps.collections.urls")),
    path(api_url_prefix, include("apps.posts.urls")),
    path(api_url_prefix, include("apps.comments.urls")),
    path(api_url_prefix, include("apps.registry.urls")),
    path(api_url_prefix, include("apps.notifications.urls")),
    path(api_url_prefix, include("apps.tye.urls")),
    path(
        f"{api_url_prefix}token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
