from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['home']

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        from django.utils import timezone
        return timezone.now() 