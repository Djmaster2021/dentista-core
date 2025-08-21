# frontend_paciente/urls.py
# Rutas públicas para el módulo de Paciente: login y registro.
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="patient_login"),
    path("registro/", views.signup_view, name="patient_signup"),
]
