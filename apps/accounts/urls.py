# apps/accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import DentistLoginView, DentistSignupView, DentistLogoutView, DashboardView
from django.contrib.auth import views as auth_views


# Rutas WEB (login / logout / registro / reset password)
webpatterns = [
    path("login/",  DentistLoginView.as_view(),   name="login"),
    path("logout/", DentistLogoutView.as_view(),  name="logout"),
    path("register/", DentistSignupView.as_view(), name="register"),
    path("dashboard/", DashboardView.as_view(),   name="dashboard"),

    # ...password reset flow con auth_views (como ya lo tenías)



    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

# Rutas API JWT
apipatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# Compat: algunos includes usan urlpatterns directamente
urlpatterns = webpatterns + apipatterns
app_name = "accounts"
