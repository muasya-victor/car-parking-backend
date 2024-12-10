from django import template

register = template.Library()

@register.filter
def sum_field(queryset, field_name):
    """Sum a specific field in a queryset."""
    return sum(getattr(obj, field_name, 0) for obj in queryset)
