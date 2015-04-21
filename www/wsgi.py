"""
WSGI config for legends project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import socket

name = socket.gethostbyaddr(socket.gethostname())[0]
os.environ["DJANGO_SETTINGS_MODULE"] = "legends.settings.{}".format(name)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
