from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index

class ResearchIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]
    
    subpage_types = ['research.ResearchPage']
    max_count = 1

    class Meta:
        verbose_name = "學術研究列表頁"

class ResearchPage(Page):
    publication_date = models.DateField("發表/公告日期")
    institution = models.CharField(max_length=255, verbose_name="研究機構/作者")
    category = models.CharField(
        max_length=50,
        choices=[
            ('SCI', 'SCI 期刊論文'),
            ('CLINICAL', '人體臨床實驗'),
            ('PATENT', '發明專利'),
            ('REPORT', '檢驗報告'),
        ],
        default='SCI',
        verbose_name="資料類別"
    )
    
    summary = RichTextField(verbose_name="研究摘要")
    
    pdf_file = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="完整文件/證書 (PDF)"
    )

    search_fields = Page.search_fields + [
        index.SearchField('institution'),
        index.SearchField('summary'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('publication_date'),
        FieldPanel('institution'),
        FieldPanel('category'),
        FieldPanel('summary'),
        FieldPanel('pdf_file'),
    ]
    
    parent_page_types = ['research.ResearchIndexPage']

    class Meta:
        verbose_name = "研究文獻/專利"
