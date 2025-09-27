from django import template

register = template.Library()

@register.filter(name="add_class")
def add_class(field, css):
    """
    Ajoute des classes CSS à un BoundField.
    Si on reçoit autre chose (str, None, etc.), on le retourne tel quel.
    """
    # Si ce n'est pas un champ de formulaire, ne rien faire
    if not hasattr(field, "as_widget") or not hasattr(field, "field"):
        return field

    widget = field.field.widget
    existing = (widget.attrs or {}).get("class", "")
    merged = (existing + " " + css).strip() if existing else css

    # On merge proprement les attrs existants
    attrs = {**(widget.attrs or {}), "class": merged}
    return field.as_widget(attrs=attrs)
