# dentist/urls.py
from django.urls import path
from . import views

app_name = "dentist"

urlpatterns = [
    path("", views.appointments_today, name="appointments_today"),
    path("appointments/<int:pk>/", views.appointment_detail, name="appointment_detail"),
    path("me/", views.me_redirect, name="me_redirect"),
]
