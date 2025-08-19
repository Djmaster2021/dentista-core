from django.shortcuts import render
from django.http import HttpResponse

# Home selector
def home(request):
    # Render a simple selector for patient/dentist portals
    return render(request, "portal/home.html")

# Patient portal
def patient_home(request):
    # Replace with your real patient dashboard template later
    return HttpResponse("Portal del Paciente - listo 👌")

# Dentist portal
def dentist_home(request):
    return render(request, "portal/dentist/appointments_list.html")

# Dentist: appointments list
def dentist_appointments_list(request):
    return render(request, "portal/dentist/appointments_list.html")

# Dentist: appointment detail
def dentist_appointment_detail(request, pk):
    return render(request, "portal/dentist/appointment_detail.html", {"pk": pk})

# Dentist: patients list
def dentist_patients_list(request):
    return render(request, "portal/dentist/patients_list.html")

# Dentist: payments list
def dentist_payments_list(request):
    return render(request, "portal/dentist/payments_list.html")