# templatetags/custom_filters.py
"""
Custom Django template filters for Excel import system
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a key
    Usage: {{ row|get_item:column_name }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key, '')
    return ''


# Backwards-compatible alias used in templates
@register.filter(name='dict_lookup')
def dict_lookup(dictionary, key):
    """
    Alias for `get_item` to support templates using `dict_lookup`.
    Usage: {{ row_data|dict_lookup:header }}
    """
    return get_item(dictionary, key)
