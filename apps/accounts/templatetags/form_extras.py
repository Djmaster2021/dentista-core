from django import template
from django.utils.safestring import mark_safe

register = template.Library()

def _merge_classes(existing: str, extra: str) -> str:
    existing_set = set((existing or "").split())
    extra_set = set((extra or "").split())
    return " ".join(sorted(existing_set.union(extra_set)))

@register.filter(name="add_class")
def add_class(field, css_classes: str):
    """
    Uso: {{ form.campo|add_class:"form-control form-control-lg" }}
    """
    widget = field.field.widget
    attrs = widget.attrs.copy()
    attrs["class"] = _merge_classes(attrs.get("class", ""), css_classes)
    return field.as_widget(attrs=attrs)

@register.filter(name="attr")
def attr(field, args: str):
    """
    Setear cualquier atributo: {{ form.campo|attr:'placeholder:Correo' }}
    También acepta múltiples: {{ form.campo|attr:'autocomplete:email,aria-label:Email' }}
    """
    widget = field.field.widget
    attrs = widget.attrs.copy()
    pairs = [p.strip() for p in args.split(",") if ":" in p]
    for pair in pairs:
        k, v = [x.strip() for x in pair.split(":", 1)]
        if k == "class":
            attrs["class"] = _merge_classes(attrs.get("class", ""), v)
        else:
            attrs[k] = v
    return field.as_widget(attrs=attrs)

@register.filter(name="is_invalid_if_errors")
def is_invalid_if_errors(field):
    """
    Agrega .is-invalid si el campo tiene errores (útil con Bootstrap)
    """
    css = "is-invalid" if field.errors else ""
    return add_class(field, css)
