"""
WSGI config for scae10 project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scae10.settings')

application = get_wsgi_application()
