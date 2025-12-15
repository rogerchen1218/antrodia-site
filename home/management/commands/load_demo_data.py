from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from home.models import HomePage, StandardPage, HomePageCarouselImages
from products.models import ProductIndexPage, ProductPage
from research.models import ResearchIndexPage, ResearchPage
import datetime

class Command(BaseCommand):
    help = 'Loads demo data for Antrodia site'

    def handle(self, *args, **options):
        self.stdout.write("Configuring Homepage...")
        # Check if a HomePage already exists
        homepage = HomePage.objects.first()
        
        if not homepage:
            root = Page.objects.get(id=1)
            
            # Check for ANY existing children (usually the Welcome page) and wipe them to ensure clean slate
            children = root.get_children()
            if children.exists():
                self.stdout.write(f"Wiping {children.count()} existing pages under Root to ensure clean state...")
                for child in children:
                    child.delete()
            
            # Force refresh and reset numchild to 0 manually to prevent Treebeard errors
            # We already have root, but let's refresh just in case delete() messed with it
            root.refresh_from_db()
            root.numchild = 0
            root.save()
            
            # Now create our HomePage
            homepage = HomePage(title="Home", slug="home")
            root.add_child(instance=homepage)
            
            homepage.title = "Antrodia 頂尖生技"
            homepage.hero_title = "源自台灣森林的紅寶石"
            homepage.hero_subtitle = "二十年固態培養技術，科學驗證的健康守護"
            
            # Add basic trust indicators (StreamField)
            # Note: StreamFields are complex to set programmatically via python shell without StreamBlock logic, 
            # but we can set simple fields easily. We will skip complex StreamField populating to avoid errors
            # and focus on main pages structure.
            
            homepage.save_revision().publish()

        # CRITICAL FIX: Set this new homepage as the "Root" of the Site
        # Otherwise Wagtail keeps showing the default "Welcome" page
        default_site = Site.objects.filter(is_default_site=True).first()
        if default_site:
            default_site.root_page = homepage
            default_site.site_name = "Antrodia Biotech"
            default_site.save()
            self.stdout.write("Updated Default Site to point to our new Homepage.")
        else:
            # Create a site if none exists (localhost)
            Site.objects.create(
                hostname='localhost',
                port=8000,
                root_page=homepage,
                is_default_site=True,
                site_name="Antrodia Biotech"
            )


        # 2. Create Product Index
        if not ProductIndexPage.objects.exists():
            self.stdout.write("Creating Product Section...")
            product_index = ProductIndexPage(
                title="精選產品",
                intro="嚴選最高品質的牛樟芝系列產品，滿足您對健康的追求。",
                slug="products"
            )
            homepage.add_child(instance=product_index)
            product_index.save_revision().publish()
        else:
            product_index = ProductIndexPage.objects.first()

        # 3. Create Sample Product
        if not ProductPage.objects.exists():
            self.stdout.write("Creating Sample Product...")
            sample_product = ProductPage(
                title="極品牛樟芝膠囊 (60粒裝)",
                product_type="B2C",
                short_description="高濃度三萜類萃取，調節生理機能的最佳選擇。",
                full_description="<p>本產品採用獨家固態培養技術，經 SGS 檢驗認證，無重金屬與農藥殘留。</p>",
                triterpenoids="12.5%",
                polysaccharides="> 8%",
                usage_instructions="<p>每日早晚各一粒，飯後食用。</p>",
                slug="premium-capsules"
            )
            product_index.add_child(instance=sample_product)
            sample_product.save_revision().publish()

        # 4. Create Research Index
        if not ResearchIndexPage.objects.exists():
            self.stdout.write("Creating Research Section...")
            research_index = ResearchIndexPage(
                title="科學驗證",
                intro="我們的每一項技術與產品，都建立在嚴謹的科學實驗基礎之上。",
                slug="research"
            )
            homepage.add_child(instance=research_index)
            research_index.save_revision().publish()
        else:
            research_index = ResearchIndexPage.objects.first()
            
        # 5. Create Sample Research
        if not ResearchPage.objects.exists():
            self.stdout.write("Creating Sample Research Paper...")
            sample_research = ResearchPage(
                title="牛樟芝三萜類對免疫細胞之影響研究",
                publication_date=datetime.date(2024, 5, 15),
                institution="國立臺灣大學醫學院",
                category="SCI",
                summary="<p>本研究證實特定濃度的牛樟芝萃取物能有效提升巨噬細胞活性...</p>",
                slug="research-paper-001"
            )
            research_index.add_child(instance=sample_research)
            sample_research.save_revision().publish()

        # 6. Create About Page
        if not StandardPage.objects.filter(slug='about').exists():
            self.stdout.write("Creating About Us Page...")
            about_page = StandardPage(
                title="關於我們",
                intro="德杏天下生技 - 專注於牛樟芝菌種培育與活性成分萃取",
                body="<p>德杏天下生物科技有限公司成立於2005年，致力於台灣特有種牛樟芝的培育與研究。我們擁有獨家的固態培養技術，能有效提升牛樟芝子實體中的三萜類與多醣體含量，並通過多項SGS檢驗認證。</p><h3>我們的核心價值</h3><ul><li><strong>科學驗證：</strong>所有產品皆經過嚴格的科學實驗與數據佐證。</li><li><strong>品質保證：</strong>從菌種培育到產品生產，全程嚴格控管。</li><li><strong>永續經營：</strong>堅持使用人工培育菌種，不採集野生牛樟芝，保護台灣森林生態。</li></ul>",
                slug="about"
            )
            homepage.add_child(instance=about_page)
            about_page.save_revision().publish()
        else:
            self.stdout.write("About Us Page already exists.")


        # 7. Create Carousel Slides
        if not HomePageCarouselImages.objects.filter(page=homepage).exists():
            self.stdout.write("Creating Carousel Slides...")
            # Slide 1
            HomePageCarouselImages.objects.create(
                page=homepage,
                title="源自台灣森林的紅寶石",
                subtitle="二十年固態培養技術，科學驗證的健康守護",
                sort_order=0
            )
            # Slide 2
            HomePageCarouselImages.objects.create(
                page=homepage,
                title="頂尖生物科技",
                subtitle="獨家萃取工藝，保存最高活性成分",
                sort_order=1
            )
            homepage.save_revision().publish()
        else:
             self.stdout.write("Carousel slides already exist.")

        self.stdout.write(self.style.SUCCESS('Successfully loaded demo data!'))
