from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.search import index

class ProductIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    subpage_types = ['products.ProductPage']
    max_count = 1

    class Meta:
        verbose_name = "產品列表頁"

class ProductPage(Page):
    # Product Details
    product_type = models.CharField(
        max_length=20,
        choices=[('B2C', '終端產品 (B2C)'), ('B2B', '保健原料 (B2B)')],
        default='B2C',
        verbose_name="產品類型"
    )
    short_description = models.TextField(blank=True, verbose_name="簡短描述")
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="產品主圖"
    )
    
    # Active Ingredients (JSON stored as text or specific fields)
    triterpenoids = models.CharField(max_length=50, blank=True, verbose_name="三萜類含量 (如 12%)")
    polysaccharides = models.CharField(max_length=50, blank=True, verbose_name="多醣體含量 (如 >5%)")

    # Full Details
    full_description = RichTextField(verbose_name="完整產品介紹")
    usage_instructions = RichTextField(blank=True, verbose_name="使用建議")
    
    # Search index configuration
    search_fields = Page.search_fields + [
        index.SearchField('short_description'),
        index.SearchField('full_description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('product_type'),
            FieldPanel('short_description'),
            FieldPanel('main_image'),
        ], heading="基本資訊"),
        MultiFieldPanel([
            FieldPanel('triterpenoids'),
            FieldPanel('polysaccharides'),
        ], heading="活性指標 (科學驗證)"),
        FieldPanel('full_description'),
        FieldPanel('usage_instructions'),
    ]
    
    parent_page_types = ['products.ProductIndexPage']

    class Meta:
        verbose_name = "產品頁面"
