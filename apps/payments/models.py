# apps/payments/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _

class PaymentMethod(models.TextChoices):
    CASH      = "CASH",      _("Efectivo")
    CARD      = "CARD",      _("Tarjeta")
    TRANSFER  = "TRANSFER",  _("Transferencia")
    MPAGO     = "MPAGO",     _("MercadoPago")

class PaymentStatus(models.TextChoices):
    PENDING   = "PENDING",   _("Pendiente")
    PAID      = "PAID",      _("Pagado")
    FAILED    = "FAILED",    _("Fallido")
    REFUNDED  = "REFUNDED",  _("Reembolsado")

# 👇 NUEVO: catálogo de monedas
class Currency(models.TextChoices):
    MXN = "MXN", "MXN"
    USD = "USD", "USD"

class Payment(models.Model):
    appointment = models.ForeignKey(
        "appointments.Appointment",
        on_delete=models.PROTECT,
        related_name="payments",
        db_index=True,
        verbose_name=_("Cita"),
    )

    amount   = models.DecimalField(_("Monto"), max_digits=10, decimal_places=2,
                                   validators=[MinValueValidator(0)])

    # 👇 CAMBIO: restringimos a choices y a 3 caracteres
    currency = models.CharField(_("Moneda"), max_length=3,
                                choices=Currency.choices, default=Currency.MXN)

    method = models.CharField(_("Método"), max_length=12,
                              choices=PaymentMethod.choices, default=PaymentMethod.CASH,
                              db_index=True)
    status = models.CharField(_("Estatus"), max_length=12,
                              choices=PaymentStatus.choices, default=PaymentStatus.PENDING,
                              db_index=True)

    external_id = models.CharField(_("ID externo"), max_length=100, blank=True, null=True)
    receipt_url = models.URLField(_("URL del recibo"), blank=True, null=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name="payments_created",
                                   verbose_name=_("Creado por"))

    created_at = models.DateTimeField(_("Creado el"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Actualizado el"), auto_now=True)

    class Meta:
        verbose_name = _("Pago")
        verbose_name_plural = _("Pagos")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "method"], name="pay_status_method_idx"),
            models.Index(fields=["appointment", "created_at"], name="pay_appt_created_idx"),
        ]
        constraints = [
            models.CheckConstraint(check=Q(amount__gte=0), name="pay_amount_gte_0"),
            models.UniqueConstraint(fields=["external_id"],
                                    name="uniq_payment_external_id_when_present",
                                    condition=Q(external_id__isnull=False)),
        ]

    def __str__(self) -> str:
        return f"Pago #{self.pk} — {self.amount} {self.currency} ({self.get_status_display()})"

    @property
    def is_paid(self) -> bool:
        return self.status == PaymentStatus.PAID

    def mark_as_paid(self):
        self.status = PaymentStatus.PAID
        self.save(update_fields=["status", "updated_at"])
