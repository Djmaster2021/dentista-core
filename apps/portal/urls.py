from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("paciente/", views.patient_home, name="patient_home"),
    path("dentista/", views.dentist_home, name="dentist_home"),
    path("dentista/citas/", views.dentist_appointments_list, name="dentist_appointments_list"),
    path("dentista/citas/<int:pk>/", views.dentist_appointment_detail, name="dentist_appointment_detail"),
    path("dentista/pacientes/", views.dentist_patients_list, name="dentist_patients_list"),
    path("dentista/pagos/", views.dentist_payments_list, name="dentist_payments_list"),
]