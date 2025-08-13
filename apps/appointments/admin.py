from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display  = ("id", "scheduled_at", "service", "full_name", "email", "phone", "status")
    list_filter   = ("status", "service", "scheduled_at", "created_at")
    search_fields = ("full_name", "email", "phone", "notes")
    ordering      = ("-scheduled_at",)
