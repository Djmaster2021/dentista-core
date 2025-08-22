from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Count

class Command(BaseCommand):
    help = "Desactiva duplicados por email conservando el más reciente; renombra usernames en conflicto."

    def handle(self, *args, **options):
        User = get_user_model()
        dupe_emails = (User.objects.exclude(email="")
                       .values('email')
                       .annotate(c=Count('id'))
                       .filter(c__gt=1))
        total_off = 0
        for row in dupe_emails:
            email = row['email']
            users = list(User.objects.filter(email=email).order_by('-date_joined','-id'))
            keep = users[0]
            for u in users[1:]:
                if u.is_active:
                    u.is_active = False
                if u.username == keep.username:
                    u.username = f"{u.username}_{u.id}"
                u.save()
                total_off += 1
        self.stdout.write(self.style.SUCCESS(f"Listo. Desactivados/renombrados: {total_off}"))
