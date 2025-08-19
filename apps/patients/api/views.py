from rest_framework import viewsets
from apps.patients.models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("-created_at")
    serializer_class = PatientSerializer
