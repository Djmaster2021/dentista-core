from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    appointment_id = serializers.IntegerField(source="appointment.id", read_only=True)
    class Meta:
        model = Payment
        fields = [
            "id", "appointment", "appointment_id",
            "amount", "currency", "method", "status",
            "external_id", "receipt_url",
            "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
