# Get the value of a key from a dictionary

from django import template

register = template.Library()

@register.filter
def get(dictionary, key):
    '''
        Get the value of key from a dictionary
    '''

    if not isinstance(dictionary, dict):
        raise TypeError('First argument to get() must be a dictionary')

    return dictionary.get(key)


