# dentist/views.py
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

# Importa el modelo real de tu app de citas
from apps.appointments.models import Appointment  # <- existente en tu repo

@login_required
def appointments_today(request):
    # Hoy, ordenado por hora. Ajusta nombres de campos si tu modelo difiere.
    qs = Appointment.objects.filter(date=date.today()).order_by("time")
    return render(request, "dentist/appointments_today.html", {"appointments": qs})

@login_required
def appointment_detail(request, pk: int):
    appt = get_object_or_404(Appointment, pk=pk)
    return render(request, "dentist/appointment_detail.html", {"appointment": appt})

def me_redirect(request):
    # Por ahora solo redirige a la lista (más adelante podemos rutear según rol)
    return redirect("dentist:appointments_today")
