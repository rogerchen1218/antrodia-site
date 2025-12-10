import os
import sys
import django
from django.conf import settings

# Minimal settings configuration
if not settings.configured:
    settings.configure(INSTALLED_APPS=['wagtail.search', 'wagtail.sites', 'wagtail.users', 'wagtail.images', 'wagtail.documents', 'wagtail', 'taggit', 'django.contrib.contenttypes', 'django.contrib.auth'])
    django.setup()

try:
    import wagtail.search.models
    print("wagtail.search.models imported successfully.")
    print("Content of wagtail.search.models:")
    print(dir(wagtail.search.models))
except ImportError as e:
    print(f"Error importing wagtail.search.models: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
