# apps/payments/apps.py
from django.apps import AppConfig

class DentyxPaymentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payments"         # ruta del paquete de TU app
    label = "dentyx_payments"      # label único para evitar choques con terceros (p.ej. django-payments)
    verbose_name = "Pagos (Dentyx)"
