from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        DENTISTA = "DENTISTA", "Dentista"
        PACIENTE = "PACIENTE", "Paciente"
        ADMIN = "ADMIN", "Administrador"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.PACIENTE)

    def __str__(self):
        return f"{self.username} ({self.role})"
