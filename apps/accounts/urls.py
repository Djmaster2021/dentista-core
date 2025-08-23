from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from .views import (
    DentistLoginView,
    DentistLogoutView,
    DentistSignupView,
    DashboardView,
)

app_name = "accounts"

# --- Rutas Web ---
webpatterns = [
    path("login/", DentistLoginView.as_view(), name="login"),
    path("logout/", DentistLogoutView.as_view(), name="logout"),
    path("register/", DentistSignupView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    # ----- Reset de contraseña -----
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

# --- Rutas API (JWT) ---
apipatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Exporta también urlpatterns para casos en que te incluyan sin 'webpatterns'
urlpatterns = webpatterns + apipatterns

urlpatterns = [
    path("accounts/", include("allauth.urls")),  # <-- rutas de allauth
]
urlpatterns = [
    path("oauth/", include("social_django.urls", namespace="social")),
]
