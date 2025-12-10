import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antrodia_project.settings")
django.setup()

from wagtail.models import Page, Site
from home.models import HomePage

print("=== Wagtail Diagnostics ===")

print(f"\n[1] Sites present: {Site.objects.count()}")
for site in Site.objects.all():
    print(f" - Site: {site.hostname}:{site.port}")
    print(f"   Is Default: {site.is_default_site}")
    print(f"   Root Page: {site.root_page} (ID: {site.root_page.id} Type: {site.root_page.specific.__class__.__name__})")

print(f"\n[2] Pages present: {Page.objects.count()}")
for page in Page.objects.all():
    print(f" - Page ID: {page.id}, Title: '{page.title}', Slug: '{page.slug}', Path: {page.path}, Live: {page.live}")
    if hasattr(page, 'specific'):
        print(f"   Type: {page.specific.__class__.__name__}")

print("\n[3] Checking Specific Models")
print(f" - HomePage objects: {HomePage.objects.count()}")

print("===========================")
