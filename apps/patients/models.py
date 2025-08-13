from django.db import models

class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "M", "Masculino"
        FEMALE = "F", "Femenino"
        OTHER = "O", "Otro"
        NA = "N", "Prefiere no decir"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.NA)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
