# apps/treatments/apps.py
from django.apps import AppConfig

class TreatmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.treatments"   # ruta real del módulo
    label = "services"         # etiqueta para que las migraciones antiguas sigan valiendo
    verbose_name = "Treatments"
