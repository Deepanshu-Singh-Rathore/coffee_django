import os

# Configure Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffee_project.settings")

from django.core.wsgi import get_wsgi_application

# WSGI application exposed for Vercel Python runtime
app = get_wsgi_application()
