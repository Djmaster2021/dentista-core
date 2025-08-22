# apps/accounts/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """
    Agrega clases CSS a un BoundField. Si llega algo que no es campo, lo devuelve tal cual.
    """
    if not hasattr(field, "as_widget"):
        return field
    base = field.field.widget.attrs.get("class", "")
    merged = f"{base} {css}".strip()
    return field.as_widget(attrs={**field.field.widget.attrs, "class": merged})

@register.filter(name="add_placeholder")
def add_placeholder(field, text):
    """
    Agrega placeholder a un BoundField. Si no es campo, lo devuelve tal cual.
    """
    if not hasattr(field, "as_widget"):
        return field
    attrs = {**field.field.widget.attrs, "placeholder": text}
    return field.as_widget(attrs=attrs)
