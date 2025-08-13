from django.db import models

class AppointmentStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Solicitada"
    CONFIRMED = "CONFIRMED", "Confirmada"
    CANCELLED = "CANCELLED", "Cancelada"
    DONE      = "DONE",      "Atendida"

class Appointment(models.Model):
    # Si el paciente ya existe en el sistema, lo enlazamos.
    # Si no, guardamos sus datos mínimos abajo (full_name/email/phone).
    patient = models.ForeignKey(
        "patients.Patient",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="appointments",
    )

    # Datos del solicitante (para permitir citas sin login)
    full_name = models.CharField(max_length=150)
    email     = models.EmailField()
    phone     = models.CharField(max_length=30)

    # Servicio y fecha/hora solicitada
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    scheduled_at = models.DateTimeField(db_index=True)

    notes  = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.REQUESTED,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-scheduled_at", "-created_at"]
        indexes = [
            models.Index(fields=["service", "scheduled_at"]),
        ]
        constraints = [
            # Evita duplicados exactos del mismo solicitante/servicio/fecha
            models.UniqueConstraint(
                fields=["full_name", "email", "phone", "service", "scheduled_at"],
                name="uniq_requester_service_datetime",
            ),
        ]

    def __str__(self):
        who = self.patient or self.full_name
        return f"{who} → {self.service} @ {self.scheduled_at:%Y-%m-%d %H:%M}"
