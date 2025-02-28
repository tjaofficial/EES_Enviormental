from django import template # type: ignore

register = template.Library()

@register.filter(name='dict_key')
def dict_key(d, key):
    """Get dictionary value by key in Django templates."""
    return d.get(key, '')

@register.filter
def get_container_field(form, field_name):
    """ Get container count field dynamically """
    index = field_name.split("_")[-1]
    return form.get(f"container_count_{index}", "")

@register.filter
def get_container_code(form, field_name):
    """ Get container waste code dynamically """
    index = field_name.split("_")[-1]
    return form.get(f"waste_code_{index}", "")

@register.filter
def get_container_dates(form, field_name):
    """ Get all waste dates for a given index """
    index = field_name.split("_")[-1]
    return [form.get(f"waste_dates_{index}_{i}", "") for i in range(10)]  # Assume max 10 dates