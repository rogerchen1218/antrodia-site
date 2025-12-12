from django.db import models

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.search import index


class HomePageCarouselImages(Orderable):
    page = ParentalKey("home.HomePage", related_name="carousel_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="輪播圖片",
    )
    title = models.CharField(max_length=100, blank=True, verbose_name="標題 (選填)")
    subtitle = models.CharField(max_length=250, blank=True, verbose_name="副標題 (選填)")

    panels = [
        FieldPanel("image"),
        FieldPanel("title"),
        FieldPanel("subtitle"),
    ]


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
        InlinePanel("carousel_images", label="輪播圖片", min_num=1),
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("trust_indicators"),
    ]

    max_count = 1  # Only one homepage allowed
    
    class Meta:
        verbose_name = "首頁"


class StandardPage(Page):
    intro = models.CharField(max_length=250, verbose_name="頁面簡介", blank=True)
    body = RichTextField(verbose_name="頁面內容")

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "通用頁面 (標準)"
