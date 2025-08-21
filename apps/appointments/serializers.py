from rest_framework import serializers
from .models import Appointment
from django.contrib.auth import get_user_model

User = get_user_model()

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, data):
        # hora fin > hora inicio
        if data["end_time"] <= data["start_time"]:
            raise serializers.ValidationError("La hora de término debe ser mayor que la de inicio.")
        return data

    def validate_dentist(self, value: User):
        # opcional: exigir dentista con rol DENTIST
        try:
            if getattr(value, "role", None) != "DENTIST":
                raise serializers.ValidationError("El usuario seleccionado no tiene rol de DENTIST.")
        except Exception:
            pass
        return value
