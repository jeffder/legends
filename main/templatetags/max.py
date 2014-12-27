# Find the maximum value in a sequence

from django import template

register = template.Library()

@register.filter
def max(values):
    '''
        Return the maximum value in values
    '''

    return max(values)


