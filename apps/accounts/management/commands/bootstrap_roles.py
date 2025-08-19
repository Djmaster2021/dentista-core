from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

ROLES = ["ADMIN", "DENTISTA", "ASISTENTE", "PACIENTE"]

# codenames típicos de tus modelos (ajusta a tus apps/modelos reales)
MODELOS = ["appointment", "patient", "payment", "penalizacion", "notificacion"]
PERMISOS = ["add", "change", "view"]  # agrega "delete" si aplica

class Command(BaseCommand):
    help = "Crea grupos básicos y asigna permisos CRUD"

    def handle(self, *args, **kwargs):
        for name in ROLES:
            g, created = Group.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(f"Grupo {name} {'creado' if created else 'ok'}"))

        # ejemplo: dar acceso CRUD a Citas/Pacientes/Pagos a DENTISTA y ASISTENTE
        for gname in ["DENTISTA", "ASISTENTE"]:
            g = Group.objects.get(name=gname)
            count_before = g.permissions.count()
            for m in MODELOS:
                for p in PERMISOS:
                    codename = f"{p}_{m}"
                    try:
                        perm = Permission.objects.get(codename=codename)
                        g.permissions.add(perm)
                    except Permission.DoesNotExist:
                        # ignora si aún no existe el modelo/permiso
                        pass
            g.save()
            self.stdout.write(self.style.SUCCESS(
                f"Permisos actualizados para {gname} (+{g.permissions.count()-count_before})"
            ))

        self.stdout.write(self.style.SUCCESS("Bootstrap de roles/permisos completo."))
