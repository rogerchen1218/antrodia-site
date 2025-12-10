import os
import django
import sys
from django.utils.text import slugify

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antrodia_project.settings")
django.setup()

from products.models import ProductPage
from research.models import ResearchPage

def fix_slugs_and_data():
    # 1. Product Pages
    print("=== Fixing Product Pages ===")
    products = ProductPage.objects.all()
    for p in products:
        updated = False
        print(f"Checking product: {p.title} (Current slug: {p.slug})")

        # Populate Missing Data
        if not p.triterpenoids:
            if "極品" in p.title:
                p.triterpenoids = "12.5%"
                p.polysaccharides = "> 8%"
            elif "大腸麵線" in p.title:
                p.triterpenoids = "0% (純粹好吃)"
                p.polysaccharides = "澱粉滿滿"
            else:
                p.triterpenoids = "檢測中"
                p.polysaccharides = "檢測中"
            updated = True
            print("  -> Populated active indicators")

        if not p.full_description or p.full_description == "":
            if "大腸麵線" in p.title:
                p.full_description = "<p>這是老闆最愛吃的古早味大腸麵線，雖然不含牛樟芝，但是吃了心情會變好，心情好免疫力自然好！嚴選台灣在地紅麵線，搭配獨門滷製大腸，湯頭濃郁不膩口。</p>"
                p.usage_instructions = "<p>熱熱吃最好吃，加點烏醋更對味。</p>"
            else:
                p.full_description = "<p>本產品採用獨家固態培養技術，經 SGS 檢驗認證，確保留有最完整的活性成分。</p>"
                p.usage_instructions = "<p>每日食用，調節生理機能。</p>"
            updated = True
            print("  -> Populated description")

        # Fix Chinese Slugs (Product)
        if any(ord(char) > 127 for char in p.slug):
            original_slug = p.slug
            if "大腸麵線" in p.title:
                new_slug = "intestine-vermicelli"
            elif "極品" in p.title:
                new_slug = "premium-capsules"
            else:
                new_slug = f"product-{p.id}"
            
            p.slug = new_slug
            updated = True
            print(f"  -> Fixed Slug: {original_slug} => {new_slug}")

        if updated:
            p.save_revision().publish()
            print("  -> Saved changes.")
        else:
            print("  -> No changes needed.")

    # 2. Research Pages
    print("\n=== Fixing Research Pages ===")
    research_pages = ResearchPage.objects.all()
    for p in research_pages:
        updated = False
        try:
            print(f"Checking research: {p.title} (Slug: {p.slug})")
        except UnicodeEncodeError:
            print(f"Checking research: (Title hidden due to encoding) (Slug: {p.slug})")
        
        # Datetime fix (sometimes usage instructions might be empty, but research usually has summaries)
        # Here we mainly focus on SLUGS
        
        # Fix Chinese Slugs (Research)
        if any(ord(char) > 127 for char in p.slug):
            original_slug = p.slug
            if "三萜類" in p.title and "免疫" in p.title:
                new_slug = "triterpenoids-immune-study"
            elif "抑制" in p.title or "癌" in p.title:
                new_slug = "antitumor-research"
            else:
                new_slug = f"research-paper-{p.id}"
            
            p.slug = new_slug
            updated = True
            print(f"  -> Fixed Slug: {original_slug} => {new_slug}")
            
        if updated:
            p.save_revision().publish()
            print("  -> Saved changes.")
        else:
            print("  -> No changes needed.")

if __name__ == "__main__":
    fix_slugs_and_data()
