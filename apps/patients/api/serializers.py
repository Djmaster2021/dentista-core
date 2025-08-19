from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.patients.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        label=_("Fecha de nacimiento"),
        input_formats=["%d/%m/%Y"],
        required=False, allow_null=True
    )
    class Meta:
        model = Patient
        fields = "__all__"
        extra_kwargs = {
            "first_name": {"label": _("Nombre")},
            "last_name":  {"label": _("Apellido")},
            "email":      {"label": _("Correo electrónico")},
            "phone":      {"label": _("Teléfono")},
            "gender":     {"label": _("Género")},
            "address":    {"label": _("Dirección"), "required": False, "allow_blank": True, "allow_null": True},
            "notes":      {"label": _("Notas"), "required": False, "allow_blank": True, "allow_null": True},
            "created_at": {"label": _("Creado el"), "read_only": True},
            "updated_at": {"label": _("Actualizado el"), "read_only": True},
        }
