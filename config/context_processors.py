# config/context_processors.py
from django.conf import settings

def theme(request):
    # Disponible como THEME en todas las plantillas
    return {"THEME": getattr(settings, "THEME", {})}
