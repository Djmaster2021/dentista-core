from django.contrib import admin
from django.apps import apps as django_apps

legacy_app = django_apps.get_app_config("legacy")

for model in legacy_app.get_models():
    # Construye un ModelAdmin genérico para cada modelo
    list_display = [f.name for f in model._meta.fields][:6]  # muestra hasta 6 campos
    search_fields = [f.name for f in model._meta.fields
                     if getattr(f, "get_internal_type", lambda: "")() in ("CharField", "TextField", "EmailField")]
    list_filter = [f.name for f in model._meta.fields if getattr(f, "choices", None)]

    admin_class = type(f"{model.__name__}Admin", (admin.ModelAdmin,), {
        "list_display": list_display or ("id",),
        "search_fields": search_fields,
        "list_filter": list_filter,
    })
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
