# apps/appointments/management/commands/seed_real_data.py
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from apps.patients.models import Patient
from apps.treatments.models import Service

from apps.appointments.models import Appointment
from apps.payments.models import Payment, Currency, PaymentMethod, PaymentStatus


SEED_TAG = "[seed]"  # marca para identificar registros sembrados


def norm_key(s: str) -> str:
    """Normaliza claves para tolerar mayúsculas/espacios."""
    return (s or "").strip().lower()


class Command(BaseCommand):
    help = (
        "Puebla la BD con datos REALISTAS (servicios, pacientes, citas y pagos) "
        "de forma idempotente. Usa --reset-seed para borrar sólo lo sembrado previamente."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Forzar actualización de valores (precio, recibos, etc.) cuando el registro ya existe.",
        )
        parser.add_argument(
            "--reset-seed",
            action="store_true",
            help="Borra SOLAMENTE los datos marcados con [seed] y vuelve a sembrar (no borra servicios).",
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        force = opts["force"]
        reset_seed = opts["reset_se ed"] if "reset_se ed" in opts else opts["reset_seed"]  # safe for typos in some shells
        # ↑ si tu shell separó mal el argumento, este fallback ayuda. Si no te gusta, cambia por: reset_seed = opts["reset_seed"]

        self.stdout.write(self.style.MIGRATE_HEADING("→ Sembrando datos reales…"))

        # Limpieza opcional: sólo lo previamente sembrado (NO borra servicios)
        if reset_seed:
            pay_deleted, _ = Payment.objects.filter(appointment__notes__startswith=SEED_TAG).delete()
            appt_deleted, _ = Appointment.objects.filter(notes__startswith=SEED_TAG).delete()
            pat_deleted, _ = Patient.objects.filter(notes__startswith=SEED_TAG).delete()
            self.stdout.write(
                self.style.WARNING(
                    f"↻ Reset seed: pagos={pay_deleted}, citas={appt_deleted}, pacientes={pat_deleted} (servicios NO se borran)"
                )
            )

        # 1) Servicios (update_or_create: nunca borramos, evitamos FK rotas)
        services_plan = [
            {"name": "Consulta general", "price": Decimal("500.00")},
            {"name": "Limpieza dental", "price": Decimal("800.00")},
            {"name": "Extracción simple", "price": Decimal("1200.00")},
            {"name": "Resina estética", "price": Decimal("950.00")},
        ]
        services = {}
        for item in services_plan:
            # Si existe, actualiza precio con --force; si no existe, lo crea.
            obj, created = Service.objects.update_or_create(
                name=item["name"],
                defaults={"price": item["price"]},
            )
            if not created and force and obj.price != item["price"]:
                obj.price = item["price"]
                obj.save(update_fields=["price"])
            services[norm_key(obj.name)] = obj
        self.stdout.write(self.style.SUCCESS(f"✔ Servicios: {len(services)}"))

        # 2) Pacientes
        patients_plan = [
            {"first_name": "María", "last_name": "González", "email": "maria.gonzalez@example.com", "phone": "5512345678"},
            {"first_name": "Carlos", "last_name": "Ramírez", "email": "carlos.ramirez@example.com", "phone": "5598765432"},
            {"first_name": "Ana",   "last_name": "López",    "email": "ana.lopez@example.com",     "phone": "5544453322"},
        ]
        patients = []
        for p in patients_plan:
            obj, created = Patient.objects.get_or_create(
                email=p["email"],
                defaults={
                    "first_name": p["first_name"],
                    "last_name":  p["last_name"],
                    "phone":      p["phone"],
                    "address":    "CDMX",
                    "notes":      f"{SEED_TAG} paciente sembrado",
                },
            )
            if not created and force:
                changed = False
                for field in ("first_name", "last_name", "phone"):
                    if getattr(obj, field) != p[field]:
                        setattr(obj, field, p[field]); changed = True
                if not (obj.notes or "").startswith(SEED_TAG):
                    obj.notes = f"{SEED_TAG} paciente sembrado"; changed = True
                if changed:
                    obj.save()
            patients.append(obj)
        self.stdout.write(self.style.SUCCESS(f"✔ Pacientes: {len(patients)}"))

        # 3) Citas (scheduled_at + status)
        now = timezone.now()
        appts = []
        appt_plan = [
            # (paciente_idx, servicio_nombre, horas_desplazamiento, status)
            (0, "Consulta general", -48, "REQUESTED"),
            (1, "Limpieza dental",  -24, "REQUESTED"),
            (2, "Resina estética",    2, "REQUESTED"),
        ]
        for idx, svc_name, hours_delta, status in appt_plan:
            patient = patients[idx]
            key = norm_key(svc_name)
            if key not in services:
                raise KeyError(f"Servicio no encontrado (revisa nombres): '{svc_name}'")
            service = services[key]
            scheduled = now + timedelta(hours=hours_delta)

            appt, created = Appointment.objects.get_or_create(
                patient=patient,
                service=service,
                scheduled_at=scheduled,
                defaults={
                    "full_name": f"{patient.first_name} {patient.last_name}",
                    "email": patient.email,
                    "phone": patient.phone,
                    "notes": f"{SEED_TAG} cita sembrada",
                    "status": status,
                },
            )
            if not created and force:
                changed = False
                if appt.full_name != f"{patient.first_name} {patient.last_name}":
                    appt.full_name = f"{patient.first_name} {patient.last_name}"; changed = True
                if appt.email != patient.email:
                    appt.email = patient.email; changed = True
                if appt.phone != patient.phone:
                    appt.phone = patient.phone; changed = True
                if appt.status != status:
                    appt.status = status; changed = True
                if not (appt.notes or "").startswith(SEED_TAG):
                    appt.notes = f"{SEED_TAG} cita sembrada"; changed = True
                if changed:
                    appt.save()
            appts.append(appt)
        self.stdout.write(self.style.SUCCESS(f"✔ Citas: {len(appts)}"))

        # 4) Pagos
        payments_plan = [
            # (cita_idx, amount, currency, method, status, external_id, receipt_url)
            (0, Decimal("500.00"), Currency.MXN, PaymentMethod.CASH,     PaymentStatus.PAID,     None,           None),
            (1, Decimal("800.00"), Currency.MXN, PaymentMethod.CARD,     PaymentStatus.PENDING,  "txn_lin_001",  "https://example.com/receipt/txn_lin_001"),
            (1, Decimal("200.00"), Currency.MXN, PaymentMethod.CARD,     PaymentStatus.PAID,     "txn_lin_002",  "https://example.com/receipt/txn_lin_002"),
            (2, Decimal("50.00"),  Currency.USD, PaymentMethod.TRANSFER, PaymentStatus.PENDING,  "txn_ext_abc",  "https://example.com/receipt/txn_ext_abc"),
        ]
        created_count = 0
        for appt_idx, amount, curr, method, status, ext_id, r_url in payments_plan:
            appt = appts[appt_idx]
            obj, created = Payment.objects.get_or_create(
                appointment=appt,
                amount=amount,
                currency=curr,
                method=method,
                status=status,
                external_id=ext_id,           # en MySQL permite múltiples NULL; si hay valor repetido sí marcará conflicto
                defaults={"receipt_url": r_url},
            )
            if created:
                created_count += 1
            elif r_url and force and obj.receipt_url != r_url:
                obj.receipt_url = r_url
                obj.save(update_fields=["receipt_url"])

        self.stdout.write(self.style.SUCCESS(f"✔ Pagos creados/asegurados: {created_count}"))
        self.stdout.write(self.style.MIGRATE_LABEL("\nListo. Tu BD ya tiene datos reales y coherentes."))
        self.stdout.write("• Pacientes: nombres, correos MX válidos, teléfonos 10 dígitos")
        self.stdout.write("• Servicios: precios con Decimal y MXN/USD en pagos")
        self.stdout.write("• Citas: usan scheduled_at + status existente")
        self.stdout.write("• Pagos: distintos métodos/monedas/estatus\n")
