"""
Base Django settings for legends project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import logging
import os


def get_environ_variable(name):
    """
    Return the variable `name` from the environment.
    """
    try:
        return os.environ[name]
    except KeyError:
        error_msg = 'Environment variable {} must be set'.format(name)
        raise ImproperlyConfigured(error_msg)


# Debug is off by default - turn it on in local settings files for dev
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['127.0.0.1']
ADMINS = (
    ('Jeff', 'jderuyter@iinet.net.au'),
)
MANAGERS = ADMINS

# Get the secret key from the environment
SECRET_KEY = '&&kkxs=@%2^s-++fdby-wagu0po7#@p%)0j@=idkh6!_*yyqe='

# Project paths
# Build paths like this: os.path.join(BASE_DIR, ...)
base_dir = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(base_dir, '..'))
MAIN_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'main'))

STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, 'static'))
TEMPLATE_DIR = os.path.abspath(os.path.join(MAIN_DIR, 'templates'))

LOG_DIR = os.path.join(PROJECT_DIR, 'log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
LOG_LEGENDS_FILE = os.path.join(LOG_DIR, 'legends.log')
LOG_RESULTS_FILE = os.path.join(LOG_DIR, 'results.log')
LOG_TIPS_FILE = os.path.join(LOG_DIR, 'tips.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s\n\t%(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s:\n\t%(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_LEGENDS_FILE,
            'formatter': 'verbose'
        },
        'tip_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_TIPS_FILE,
            'formatter': 'simple'
        },
        'result_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_RESULTS_FILE,
            'formatter': 'simple'
        }
    },
    'loggers': {
        'legends': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'legends.tip': {
            'handlers': ['tip_file'],
            'level': 'INFO',
            'propagate': False
        },
        'legends.result': {
            'handlers': ['result_file'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'mod_wsgi.server',
    # Legends apps
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_DIR,
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'legends.urls'

WSGI_APPLICATION = 'www.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
# We don't want internationalization
USE_I18N = False
USE_I10N = True

# Time

TIME_ZONE = 'Australia/Melbourne'
TIME_FORMAT = 'Y-m-d H:i:s EST'
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# Set ADMIN_MEDIA_PREFIX in local_settings/<hostname>.py
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

AUTH_PROFILE_MODULE = "main.models.club"
LOGIN_REDIRECT_URL = '/legends/'
LOGIN_URL = '/accounts/login/'

# Use syncdb to make the test database
SOUTH_TESTS_MIGRATE = False
