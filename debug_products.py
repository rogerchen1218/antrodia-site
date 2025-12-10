
import os
import django
import sys

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antrodia_project.settings")
django.setup()

from products.models import ProductPage, ProductIndexPage
from wagtail.models import Site

print("=== Site Configuration ===")
for site in Site.objects.all():
    print(f"Site: {site.hostname} [default={site.is_default_site}] Root Page: {site.root_page}")

print("\n=== Product Index Pages ===")
indices = ProductIndexPage.objects.all()
for p in indices:
    print(f"Title: {p.title}, Slug: {p.slug}, URL: {p.get_url()}, Live: {p.live}")

print("\n=== Product Pages ===")
products = ProductPage.objects.all()
for p in products:
    print(f"Title: {p.title}, Slug: {p.slug}, URL: {p.get_url()}, Live: {p.live}, Parent: {p.get_parent().title}")
