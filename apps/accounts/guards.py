# apps/accounts/guards.py
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

def staff_required(view_func):
    """
    Permite solo usuarios autenticados con is_staff=True.
    """
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(view_func)

# Útil si luego quieres vistas para paciente autenticado
login_required_custom = login_required
