from rest_framework import viewsets, permissions
from apps.appointments.models import Appointment
from .serializers import AppointmentSerializer  

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = (Appointment.objects
                .select_related("patient", "service")
                .order_by("-scheduled_at"))
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
