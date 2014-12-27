# Find the sum of the values in a sequence

from django import template

register = template.Library()

@register.filter
def sum(values):
    '''
        Return the sum of the values in values
    '''

    if not values:
        return 0
    
    if isinstance(values, GeneratorType):
        values = list(values)

    try:
        return sum(values)

    except:
        raise TypeError('Values must be a sequence of numeric values')


