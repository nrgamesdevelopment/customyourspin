from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return [
            'home',  # Main homepage
            'blog',  # Blog section
            'about', # About section
            'partners' # Partners section
        ]

    def location(self, item):
        if item == 'home':
            return reverse('home')
        else:
            # For sections that are on the same page, use anchors
            return f"{reverse('home')}#{item}"
    
    def lastmod(self, obj):
        return timezone.now()

class BlogSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        # Return blog-related content or sections
        return [
            'spin-wheel-generator-india-2025',
            'instagram-reels-wheel-challenges',
            'youtube-shorts-wheel-challenges', 
            'classroom-spinner-tool-india',
            'giveaway-wheel-generator-india',
            'decision-maker-wheel-india',
            'free-online-spinner-india',
            'custom-wheel-maker-india',
            'random-picker-tool-india'
        ]

    def location(self, item):
        # These are sections within the main page, so use anchors
        return f"{reverse('home')}#blog"
    
    def lastmod(self, obj):
        return timezone.now()

# Update the sitemaps dictionary in urls.py to include both
sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
} 