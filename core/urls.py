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
    path("news/", include("news.core.urls")),
    path("crud/", include("crud.core.urls")),
    path("bank/", include("bank.core.urls")),
    path("ml/", include("ml.core.urls")),
    path("payments/", include("payments.core.urls")),
    path("paypal_payments/", include("paypal_payments.core.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
