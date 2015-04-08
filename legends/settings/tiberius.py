"""
Local Django settings for legends project on tiberius.
"""

import os

from legends.settings.base import *

# We want debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1', '192.168.1.103', '192.168.1.116')

# Project paths
SQLITE_DB_NAME = os.path.join(PROJECT_DIR, 'legends.db')
TEST_DB_NAME = os.path.join(PROJECT_DIR, 'test_legends3.fdb')

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'firebird',
        'NAME': 'legends3',           # Path to database or db alias
        'USER': 'legends',            # Your db user
        'PASSWORD': 'saintssaints',   # db user password
        'HOST': '127.0.0.1',          # Your host machine
        'PORT': '3050',               # If is empty, use default 3050
        'OPTIONS': {'charset': 'UTF8'},
        'TEST_NAME': TEST_DB_NAME
    },
    'old': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': SQLITE_DB_NAME
    },
    'old_fb': {
        'ENGINE': 'firebird',
        'NAME': 'legends',           # Path to database or db alias
        'USER': 'legends',            # Your db user
        'PASSWORD': 'saintssaints',   # db user password
        'HOST': 'nero',          # Your host machine
        'PORT': '3050',               # If is empty, use default 3050
        'OPTIONS': {'charset': 'ISO8859_1'},
        'TEST_NAME': TEST_DB_NAME
    },
}

INSTALLED_APPS += (
    'django_extensions',
)

TEMPLATE_STRING_IF_INVALID = 'XXX'
