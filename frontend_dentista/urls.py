# frontend_dentista/urls.py
# Rutas públicas para el módulo de Dentista: login y registro.
from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="dentist_login"),
    path("registro/", views.signup_view, name="dentist_signup"),
]
