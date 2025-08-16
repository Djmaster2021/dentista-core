from django.db import models
from django.conf import settings

class PaymentMethod(models.TextChoices):
    CASH      = "CASH",      "Efectivo"
    CARD      = "CARD",      "Tarjeta"
    TRANSFER  = "TRANSFER",  "Transferencia"
    MPAGO     = "MPAGO",     "MercadoPago"

class PaymentStatus(models.TextChoices):
    PENDING   = "PENDING",   "Pendiente"
    PAID      = "PAID",      "Pagado"
    FAILED    = "FAILED",    "Fallido"
    REFUNDED  = "REFUNDED",  "Reembolsado"

class Payment(models.Model):
    # Relación a la cita (pago por una consulta/servicio)
    appointment = models.ForeignKey(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="payments",
        db_index=True,
    )

    # Monto y moneda
    amount   = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="MXN")

    # Método y estatus
    method = models.CharField(
        max_length=12,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        db_index=True,
    )
    status = models.CharField(
        max_length=12,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )

    # Identificadores externos (ej. MercadoPago) y recibo
    external_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    receipt_url = models.URLField(blank=True, null=True)

    # Quién registró (opcional)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="payments_created",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "method"]),
        ]

    def __str__(self) -> str:
        return f"Pago #{self.pk} — {self.amount} {self.currency} ({self.get_status_display()})"
