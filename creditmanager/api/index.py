import os
import sys

# Make sure the root project folder is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from creditmanager.wsgi import application as django_app

# Vercel expects a top-level variable named `app` or `handler`
app = django_app
