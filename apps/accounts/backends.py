from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        # Filtra por username/email (case-insensitive) y solo activos
        qs = User.objects.filter(
            Q(username__iexact=username) | Q(email__iexact=username),
            is_active=True
        ).order_by('id')  # el más antiguo primero

        user = qs.first()  # evita MultipleObjectsReturned
        if not user:
            return None
        if user.check_password(password):
            return user
        return None
