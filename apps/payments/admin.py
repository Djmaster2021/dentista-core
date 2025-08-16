from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "appointment", "amount", "currency", "method", "status", "created_at")
    list_filter  = ("status", "method", "currency", "created_at")
    search_fields = ("external_id",)
    autocomplete_fields = ("appointment", "created_by")
