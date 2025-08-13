from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Schema & docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Apps
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/patients/", include("apps.patients.urls")),
    path("api/services/", include("apps.services.urls")),
    path("api/appointments/", include("apps.appointments.urls")),
]
