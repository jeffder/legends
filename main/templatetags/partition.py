# Split a list into into equally sized parts

from django import template

register = template.Library()

@register.filter
def partition(values, size = 2):
    '''
        Split a list of values into lists of equal size.
        The default size is 2.
    '''
    
    if not isinstance(size, int):
        size = int(size)

    if size <= 0:
        size = 2

    return [values[start:start + size] for start in xrange(0, len(values), size)]


