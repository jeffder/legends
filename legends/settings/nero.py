"""
Local Django settings for legends project on nero.
"""

import os

from legends.settings.base import *


DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'firebird',
        'NAME': 'legends',      # Path to database or db alias
        'USER': 'legends',       # Your db user
        'PASSWORD': 'saintssaints',   # db user password
        'HOST': '127.0.0.1',     # Your host machine
        'PORT': '3050',          # If is empty, use default 3050
        'OPTIONS': {'charset': 'ISO8859_1'},
    }
}
