from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks


class HomePage(Page):
    # Hero Section
    hero_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="首頁大標題")
    hero_subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="首頁副標題")
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="首頁背景圖",
    )

    # Trust Benefit Section (StreamField)
    trust_indicators = StreamField(
        [
            ("benefit", blocks.StructBlock([
                ("title", blocks.CharBlock(label="優勢標題")),
                ("description", blocks.TextBlock(label="優勢說明")),
                ("icon_class", blocks.CharBlock(label="圖示代碼 (如 fa-shield)", required=False)),
            ], label="信任指標")),
        ],
        use_json_field=True,
        null=True,
        blank=True,
        verbose_name="信任指標區塊",
    )

    content_panels = Page.content_panels + [
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("trust_indicators"),
    ]

    max_count = 1  # Only one homepage allowed
    
    class Meta:
        verbose_name = "首頁"
