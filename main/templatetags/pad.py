# Pad a string with nbsp;

from django import template

register = template.Library()


@register.filter
def pad(value, size=0):
    """
    Pad a string with nbsp; so the it's length is size e.g 'foo'|pad(5) returns
    '&nbsp;&nbsp;foo'.
    Return the string if it is longer than size.
    """
    if not isinstance(value, str):
        value = str(value)

    val_size = len(value)

    if val_size >= size:
        return value

    fill_size = size - val_size

    return '{}{}'.format('&nbsp;' * fill_size, value)