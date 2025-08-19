from rest_framework import viewsets, filters
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related("appointment").all().order_by("-created_at")
    serializer_class = PaymentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["external_id", "appointment__patient__first_name", "appointment__patient__last_name"]
    ordering_fields = ["created_at", "amount", "status", "method"]
