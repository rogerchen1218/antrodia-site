import os

path = r"c:/Users/User/OneDrive/Desktop/web test/home/templates/home/home_page.html"
html = """{% extends "base.html" %}
{% load wagtailcore_tags wagtailimages_tags %}

{% block content %}
{# Hero Section #}
<div class="hero-section" {% if page.hero_image %}style="background-image: url('{{ page.hero_image.file.url }}'); background-size: cover; background-position: center;"{% endif %}>
    <div class="container hero-content">
        <h1 class="hero-title">{{ page.hero_title }}</h1>
        <p class="hero-subtitle">{{ page.hero_subtitle }}</p>
        <a href="/products/" class="btn btn-primary">探索我們的產品</a>
    </div>
</div>

{# Trust Indicators #}
{% if page.trust_indicators %}
<div class="trust-section">
    <div class="container">
        <h2 style="text-align: center; color: var(--primary-color);">為什麼選擇我們？</h2>
        <div class="trust-grid">
            {% for block in page.trust_indicators %}
            <div class="trust-card">
                <div class="trust-icon">
                    {% if block.value.icon_class %}
                    <i class="{{ block.value.icon_class }}"></i>
                    {% else %}
                    ★
                    {% endif %}
                </div>
                <h3>{{ block.value.title }}</h3>
                <p>{{ block.value.description }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endif %}

{# Simple About Teaser #}
<div class="container" style="padding: 100px 20px; text-align: center;">
    <h2 style="color: var(--primary-color); margin-bottom: 20px;">源自科學，忠於純粹</h2>
    <p style="max-width: 800px; margin: 0 auto; color: #666;">
        我們堅持使用經過基因鑑定的野生牛樟芝菌種，利用獨家固態培養技術，
        確保每一份原料都含有高濃度的三萜類與多醣體。
    </p>
</div>
{% endblock %}
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Fix executed.")
