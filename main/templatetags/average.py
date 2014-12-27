# Find the average value in a sequence

from django import template

register = template.Library()

@register.filter
def average(values):
    '''
        Return the average value in values
    '''

    if not values:
        raise ValueError('Attempting to find the average of an empty sequence.')
    
    if isinstance(values, GeneratorType):
        values = list(values)

    try:
        count = len(values)

        return float(sum(values)) / count

    except:
        raise TypeError('Values must be a sequence of numeric values')


