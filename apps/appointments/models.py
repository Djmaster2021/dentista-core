from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Agendada"
        CONFIRMED = "CONFIRMED", "Confirmada"
        CANCELLED = "CANCELLED", "Cancelada"
        COMPLETED = "COMPLETED", "Completada"

    patient = models.ForeignKey("patients.Patient", on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey("services.Service", on_delete=models.PROTECT, related_name="appointments")
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, related_name="appointments_as_dentist")

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.SCHEDULED)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-start_time"]

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time} • {self.patient} • {self.service}"
