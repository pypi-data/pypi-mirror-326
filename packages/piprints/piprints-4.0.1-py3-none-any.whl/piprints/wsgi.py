import os
import sys
import site
from django import settings

sys.path.append(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'piprints.settings'

PROJECT_ROOT = os.path.abspath(os.path.join(settings.BASE_ROOT, '..'))
sys.path.append(PROJECT_ROOT)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
