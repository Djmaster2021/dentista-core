from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.appointments.models import Appointment

User = get_user_model()


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, data):
        # ejemplo: scheduled_at no en el pasado
        scheduled = data.get("scheduled_at") or getattr(self.instance, "scheduled_at", None)
        from django.utils import timezone
        if scheduled and scheduled < timezone.now():
            raise serializers.ValidationError({"scheduled_at": "No puedes agendar en el pasado."})
        return data

    # ← importante: SIN tipado aquí
    def validate_dentist(self, value):
        """
        Si tu Appointment tiene FK 'dentist', validamos que el usuario sea dentista/staff.
        Si no usas ese campo, puedes borrar este método.
        """
        if value is None:
            return value
        # ajusta a tu lógica real: role / is_staff / permisos, etc.
        role = getattr(value, "role", None)
        if role and role != "DENTIST":
            raise serializers.ValidationError("El usuario seleccionado no es dentista.")
        if not getattr(value, "is_staff", False):
            raise serializers.ValidationError("Debe ser personal autorizado (staff).")
        return value
