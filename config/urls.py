from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Login/Logout de la UI de DRF (sesiones, muy útil para probar en el navegador)
    path("api-auth/", include("rest_framework.urls")),

    # JWT endpoints (para tu front/app)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Rutas de tus apps
    path("", include("apps.accounts.urls")),
    path("", include("apps.patients.urls")),
    path("", include("apps.appointments.urls")),
    path("", include("apps.services.urls")),
    # path("", include("apps.payments.urls")),  # cuando lo tengamos
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
