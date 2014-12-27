# Split a list into into equally sized parts

from itertools import zip_longest

from django import template

register = template.Library()


@register.filter
def chop(values, size=2):
    '''
        Split a list of values into lists of equal size.
        For example chop([1, 2, 3, 4]) returns [(1, 2), (3, 4)].
        The default size is 2.
    '''

    if not isinstance(size, int):
        raise TypeError('Size must be an integer')

    if size <= 0:
        size = 2

    return zip_longest(*(iter(values),) * size, fillvalue='')
