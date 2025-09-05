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
        # Keep this list in sync with ads.views.ARTICLES
        return [
            'spin-wheel-generator-india-2025',
            'instagram-reels-wheel-challenges',
            'youtube-shorts-wheel-challenges',
            'classroom-spinner-tool-india',
            'giveaway-wheel-generator-india',
            'decision-maker-wheel-india',
            'free-online-spinner-india',
            'custom-wheel-maker-india',
            'random-picker-tool-india',
            'party-game-wheel-ideas',
            'team-building-wheel-activities',
            'study-roulette-for-students',
            'truth-or-dare-wheel-template',
            'this-or-that-wheel-questions',
            'workout-challenge-wheel',
            'teachers-random-name-picker',
            'spin-wheel-for-streamers',
            'restaurant-menu-chooser',
            'date-night-decision-wheel',
            'classroom-behavior-rewards-wheel',
            'quiz-and-trivia-randomizer',
            'lucky-draw-and-raffle-guide',
            'wedding-games-wheel',
            'festival-games-diwali-holi',
            'school-assembly-selector',
            'corporate-giveaway-ideas',
            'spin-wheel-seo-benefits',
            'privacy-and-safety-on-cyw',
            'how-to-embed-the-wheel',
            'accessibility-features',
        ]

    def location(self, item):
        return reverse('blog_article', args=[item])
    
    def lastmod(self, obj):
        return timezone.now()

# Update the sitemaps dictionary in urls.py to include both
sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
} 