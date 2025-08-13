# config/urls.py
from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import DentistLoginView, root_redirect
from apps.accounts import urls as accounts_urls

urlpatterns = [
    # 👇 raíz: si está logueado -> /dashboard/, si no -> /login/
    path("", root_redirect, name="root"),

    # Admin usando tu login
    path("admin/login/", DentistLoginView.as_view(), name="admin_login"),
    path("admin/", admin.site.urls),

    # WEB (login, logout, register, reset...) con namespace "accounts"
    path("", include((accounts_urls.webpatterns, "accounts"), namespace="accounts")),

    # API JWT debajo de /api/accounts/ con su propio namespace
    path(
        "api/accounts/",
        include((accounts_urls.apipatterns, "accounts_api"), namespace="accounts_api"),
    ),

    # Otras APIs si aplica:
    # path("api/patients/", include("apps.patients.urls")),
    # path("api/services/", include("apps.services.urls")),
    # path("api/appointments/", include("apps.appointments.urls")),
]
