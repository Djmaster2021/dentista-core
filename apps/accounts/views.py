# apps/accounts/views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView  # usamos las vistas de auth
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

# Tus formularios (si cambian de nombre, ajústalo aquí)
from .forms import DentistAuthForm, DentistSignupForm

User = get_user_model()


class DentistLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = DentistAuthForm
    redirect_authenticated_user = True


class DentistLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class DentistSignupView(CreateView):
    form_class = DentistSignupForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"
    login_url = "accounts:login"
    redirect_field_name = "next"


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return redirect("accounts:login")
