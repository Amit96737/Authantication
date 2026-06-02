from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings
from .api_urls import urlpatterns as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path("", include("dashboard.core.urls")),
    path("ai/", include("ai.core.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
