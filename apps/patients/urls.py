from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet

router = DefaultRouter()
router.register(r"", PatientViewSet, basename="patient")  # quedará en /api/patients/

urlpatterns = [
    path("", include(router.urls)),
]
