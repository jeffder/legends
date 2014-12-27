# Miscellaneous utilities

from itertools import zip_longest


def chunks(values, size=2, fill=None):
    """
    Split a list of values into chunks of equal size.
    For example chunks([1, 2, 3, 4]) returns [(1, 2), (3, 4)].
    The default size is 2.
    :param values: the iterable to be split into chunks
    :param size: the size of the chunks. Must be an integer.
    :param fill: fill missing values in with fill value
    """
    if not isinstance(size, int):
        raise TypeError('Size must be an integer')

    if size <= 0:
        size = 2

    return zip_longest(*(iter(values),) * size, fillvalue=fill)
