from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    # decide por rol/flag. Ej: staff = dentista
    if user.is_staff or user.is_superuser:
        return redirect("dentist:appointment_list")  # sin dashboard
    # paciente (ajusta a tu app real de pacientes/portal)
    return redirect("frontend_paciente:home")  # o donde toque
