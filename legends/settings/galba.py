"""
Local Django settings for legends project on galba.
"""

import os

from legends.settings.base import *


# We don't want debugging in production
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Project paths
SQLITE_DB_NAME = os.path.join(PROJECT_DIR, 'legends.db')

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'firebird',
        'NAME': 'legends',           # Path to database or db alias
        'USER': 'legends',            # Your db user
        'PASSWORD': 'saintssaints',   # db user password
        'HOST': '127.0.0.1',          # Your host machine
        'PORT': '3050',               # If is empty, use default 3050
        'OPTIONS': {'charset': 'UTF8'},
    },
    'old': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SQLITE_DB_NAME,
    }
}

TEMPLATE_STRING_IF_INVALID = ''
