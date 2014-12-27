# Split a list into into two equal halves

from django import template

register = template.Library()

@register.filter
def split(values):
    '''
        Split a list of values into two equal sized lists.
    '''

    size = len(values)
    half_size = len(values) / 2
    if size % 2:
        half_size += 1

    return (values[:half_size], values[half_size:])


