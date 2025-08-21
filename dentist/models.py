from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Patient(models.Model):
    full_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.full_name

class Service(models.Model):
    name = models.CharField(max_length=80)
    price_mxn = models.DecimalField(max_digits=9, decimal_places=2)
    active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Appointment(models.Model):
    STATUS = [
        ("scheduled","Agendada"),("confirmed","Confirmada"),
        ("done","Atendida"),("cancelled","Cancelada"),("no_show","No asistió"),
    ]
    dentist = models.ForeignKey(User, on_delete=models.PROTECT, related_name="appointments")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=12, choices=STATUS, default="scheduled")
    paid_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("dentist","date","time")
        ordering = ["-date","-time"]
    def __str__(self): return f"{self.patient} · {self.date} {self.time}"

class Payment(models.Model):
    METHOD = [("cash","Efectivo"),("card","Tarjeta"),("online","En línea")]
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="payment")
    amount_mxn = models.DecimalField(max_digits=9, decimal_places=2)
    method = models.CharField(max_length=10, choices=METHOD)
    reference = models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"${self.amount_mxn} · {self.method}"
