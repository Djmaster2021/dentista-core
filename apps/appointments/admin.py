from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "start_time", "end_time", "patient", "service", "dentist", "status")
    list_filter = ("status", "date", "dentist")
    search_fields = ("patient__first_name", "patient__last_name", "service__name", "dentist__username")
