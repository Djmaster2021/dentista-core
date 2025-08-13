from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "duration_minutes", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("name",)
