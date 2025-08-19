# apps/patients/models.py
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", _("Masculino")
        FEMALE = "F", _("Femenino")
        OTHER = "O", _("Otro")

    phone_validator = RegexValidator(r"^\d{10}$", message=_("Ingresa un número de 10 dígitos (solo números)."))

    first_name = models.CharField(_("Nombre"), max_length=100)
    last_name  = models.CharField(_("Apellido"), max_length=100)

    # ÚNICO y normalizable; el UniqueConstraint de abajo lo asegura case-insensitive (ideal si usas PostgreSQL)
    email      = models.EmailField(_("Correo electrónico"), unique=True)

    # Opcional: si quieres forzar unicidad de teléfono, descomenta unique=True
    phone      = models.CharField(_("Teléfono"), max_length=20, validators=[phone_validator, MinLengthValidator(10)])
    birth_date = models.DateField(_("Fecha de nacimiento"), null=True, blank=True)
    gender     = models.CharField(_("Género"), max_length=1, choices=Gender.choices, default=Gender.MALE)

    address    = models.CharField(_("Dirección"), max_length=255, blank=True, default="")
    notes      = models.TextField(_("Notas"), blank=True, default="")

    created_at = models.DateTimeField(_("Creado el"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Actualizado el"), auto_now=True)

    class Meta:
        verbose_name = _("Paciente")
        verbose_name_plural = _("Pacientes")
        ordering = ("-created_at",)

        # Índices útiles para búsquedas comunes
        indexes = [
            models.Index(fields=["last_name", "first_name"], name="patient_name_idx"),
            models.Index(fields=["phone"], name="patient_phone_idx"),
            models.Index(fields=["created_at"], name="patient_created_idx"),
        ]

        # Reglas extra de unicidad
        # Email case-insensitive (requiere PostgreSQL para funcionar perfecto)
        constraints = [
            models.UniqueConstraint(Lower("email"), name="uniq_patient_email_lower"),
            # Si quieres que teléfono sea único, descomenta esto:
            # models.UniqueConstraint(Lower("phone"), name="uniq_patient_phone_lower"),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
