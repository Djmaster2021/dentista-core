# dentist/apps.py
from django.apps import AppConfig

class DentistCoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dentist"          # carpeta de la app core
    label = "dentist_core"    # label único
    verbose_name = "Dentista Core"
