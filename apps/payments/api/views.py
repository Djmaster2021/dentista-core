from rest_framework import viewsets, permissions
from apps.payments.models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("appointment").all().order_by("-created_at")
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
