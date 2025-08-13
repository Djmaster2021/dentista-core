from rest_framework import viewsets, permissions
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("patient", "service", "dentist").all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
