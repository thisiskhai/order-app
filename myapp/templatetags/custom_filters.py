# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    return d.get(key)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def sum_attr(items, attr):
    return sum(getattr(item, attr, 0) for item in items)
