from django.contrib import admin
from .models import Patient, Service, Appointment, Payment

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ("full_name","email","phone")
    list_display = ("full_name","email","phone","created_at")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name","price_mxn","active")
    list_editable = ("price_mxn","active")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("date","time","patient","service","status","paid_online")
    list_filter = ("status","paid_online","date","service")
    search_fields = ("patient__full_name","notes")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("appointment","amount_mxn","method","reference","created_at")
