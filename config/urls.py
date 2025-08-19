from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.templatetags.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Portal (home, paciente, dentista)
    path("", include(("apps.portal.urls", "portal"), namespace="portal")),

    # Auth
    path("accounts/", include(("apps.accounts.urls", "accounts"), namespace="accounts")),

    # APIs (v1)
    path("api/v1/appointments/", include("apps.appointments.api.urls")),
    path("api/v1/patients/", include("apps.patients.api.urls")),
    path("api/v1/payments/", include("apps.payments.api.urls")),
    path("favicon.ico", RedirectView.as_view(url=static("favicon.ico"), permanent=True)),
    # Catálogo de tratamientos (no-API, vistas server-side)
    path("treatments/", include(("apps.treatments.urls", "treatments"), namespace="treatments")),
]
