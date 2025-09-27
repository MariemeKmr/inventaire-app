from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    # Concatène proprement la classe existante et la nouvelle
    existing = field.field.widget.attrs.get("class", "")
    merged = (existing + " " + css).strip()
    attrs = {**field.field.widget.attrs, "class": merged}
    return field.as_widget(attrs=attrs)

@register.filter(name="add_attr")
def add_attr(field, arg):
    """
    Usage : {{ field|add_attr:"placeholder:Votre email" }}
            {{ field|add_attr:"class:form-control is-invalid" }}
    """
    if ":" not in arg:
        return field
    key, value = arg.split(":", 1)
    attrs = field.field.widget.attrs.copy()
    if key == "class":
        attrs["class"] = (attrs.get("class", "") + " " + value).strip()
    else:
        attrs[key] = value
    return field.as_widget(attrs=attrs)
