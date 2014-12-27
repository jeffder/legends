# Find the minimum value in a sequence

from django import template

register = template.Library()

@register.filter
def min(values):
    '''
        Return the minimum value in values
    '''

    return min(values)


