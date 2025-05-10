"""
WSGI config for steam_downgrade project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steam_downgrade.settings')

application = get_wsgi_application()
