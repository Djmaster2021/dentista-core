# apps/appointments/api/serializers.py
from rest_framework import serializers
from apps.appointments.models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Appointment
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")
