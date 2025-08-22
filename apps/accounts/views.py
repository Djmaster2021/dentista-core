from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View

from .forms import DentistAuthForm, DentistSignupForm


def root_redirect(request):
    """
    / -> si está logueado va al dashboard, si no al login.
    (Útil si en config/urls.py pones path('', root_redirect, ...))
    """
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return redirect("accounts:login")


class DentistLoginView(LoginView):
    """
    Vista de inicio de sesión (usa el form del proyecto).
    """
    template_name = "accounts/login.html"
    authentication_form = DentistAuthForm
    redirect_authenticated_user = True

    def get_success_url(self):
        # Tras autenticarse, ir al dashboard
        return reverse_lazy("accounts:dashboard")


class DentistLogoutView(LogoutView):
    """
    Cierra sesión y regresa al login.
    Acepta GET y POST para evitar 405 si el usuario pega la URL en la barra.
    """
    next_page = reverse_lazy("accounts:login")
    http_method_names = ["get", "post", "options", "head"]


class DentistSignupView(View):
    """
    Registro de nuevo dentista.
    GET: muestra formulario
    POST: valida, crea usuario, inicia sesión y redirige al dashboard.
    """
    template_name = "accounts/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("accounts:dashboard")
        form = DentistSignupForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = DentistSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # el form debe hacer set_password y validaciones
            # Autenticar con las credenciales recién creadas
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(request, username=email or user.username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, "¡Cuenta creada y sesión iniciada!")
                return redirect("accounts:dashboard")
            messages.info(request, "Cuenta creada. Inicia sesión para continuar.")
            return redirect("accounts:login")
        # Si no es válido, re-render con errores
        return render(request, self.template_name, {"form": form})


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard del dentista.
    """
    template_name = "portal/home.html"
    login_url = reverse_lazy("accounts:login")
