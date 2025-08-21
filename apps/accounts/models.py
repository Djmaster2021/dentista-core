from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        DENTIST = "DENTIST", "Dentist"
        PATIENT = "PATIENT", "Patient"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
        help_text="Rol del usuario dentro del sistema",
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
# accounts/models.py (tu CustomUser)
phone = models.CharField(
    max_length=20,
    unique=True,
    null=True,    # <- permite NULL en BD
    blank=True,   # <- no lo exige en formularios/createsuperuser
)

