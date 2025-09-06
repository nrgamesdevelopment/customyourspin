from django.shortcuts import render
from django.http import JsonResponse
from .models import Ad
from django.http import HttpResponse
import os
from pathlib import Path
from django.http import Http404

# Create your views here.

def latest_ad(request):
    ad = Ad.objects.order_by('-id').first()
    if ad:
        data = {
            'ad_name': ad.ad_name,
            'image': request.build_absolute_uri(ad.image.url),
            'link': ad.link,
        }
    else:
        data = {}
    return JsonResponse(data)

# New view for all ads

def all_ads(request):
    ads = Ad.objects.order_by('-id')
    data = [
        {
            'ad_name': ad.ad_name,
            'image': request.build_absolute_uri(ad.image.url),
            'link': ad.link,
        }
        for ad in ads
    ]
    return JsonResponse({'ads': data})

def home(request):
    return render(request, 'home.html')

# -------------------- Blog --------------------
# Central registry for blog articles. Keep slug => meta mapping here
ARTICLES = [
    {
        'slug': 'spin-wheel-generator-india-2025',
        'title': 'Free Spin Wheel Generator (India, 2025) – Custom Your Spin',
        'description': 'Create free spin wheels instantly for games, giveaways and decisions.'
    },
    {
        'slug': 'instagram-reels-wheel-challenges',
        'title': 'Instagram Reels Wheel Challenges – Ideas that Go Viral',
        'description': 'Use our wheel to create engaging Reels challenges and trends.'
    },
    {
        'slug': 'youtube-shorts-wheel-challenges',
        'title': 'YouTube Shorts Wheel Challenges – Quick Video Ideas',
        'description': 'Generate Shorts content ideas with a single spin.'
    },
    {
        'slug': 'classroom-spinner-tool-india',
        'title': 'Classroom Spinner Tool for Teachers in India',
        'description': 'Pick students, topics and activities fairly in class.'
    },
    {
        'slug': 'giveaway-wheel-generator-india',
        'title': 'Giveaway Wheel Generator – Fair, Fun, and Transparent',
        'description': 'Run audience giveaways with clarity and excitement.'
    },
    {
        'slug': 'decision-maker-wheel-india',
        'title': 'Decision Maker Wheel – Decide Anything Fast',
        'description': 'Flip a coin, spin a wheel, or pick randomly when stuck.'
    },
    {
        'slug': 'free-online-spinner-india',
        'title': 'Free Online Spinner – No Sign-up, No Download',
        'description': 'Launch the spinner instantly from any browser.'
    },
    {
        'slug': 'custom-wheel-maker-india',
        'title': 'Custom Wheel Maker – Colors, Themes and Templates',
        'description': 'Build wheels your way with themes like pizza, chips and coin.'
    },
    {
        'slug': 'random-picker-tool-india',
        'title': 'Random Picker Tool – Names, Numbers and More',
        'description': 'Fair random selection for names, numbers and prizes.'
    },
    { 'slug': 'party-game-wheel-ideas', 'title': 'Party Game Wheel – 25 Fun Ideas', 'description': 'Instant party starters for birthdays and house parties.' },
    { 'slug': 'team-building-wheel-activities', 'title': 'Team Building with the Wheel', 'description': 'Icebreakers and activities for teams.' },
    { 'slug': 'study-roulette-for-students', 'title': 'Study Roulette – Make Learning Fun', 'description': 'Gamify revision and topic selection.' },
    { 'slug': 'truth-or-dare-wheel-template', 'title': 'Truth or Dare Wheel Template', 'description': 'Ready-to-use list for classic fun.' },
    { 'slug': 'this-or-that-wheel-questions', 'title': 'This or That – 200+ Prompts', 'description': 'Quick conversation starter prompts.' },
    { 'slug': 'workout-challenge-wheel', 'title': 'Workout Challenge Wheel', 'description': 'Randomize exercises for fitness.' },
    { 'slug': 'teachers-random-name-picker', 'title': 'Teacher’s Random Name Picker', 'description': 'Call on students fairly with a spin.' },
    { 'slug': 'spin-wheel-for-streamers', 'title': 'Spin Wheel for Streamers', 'description': 'Engage your live audience on YouTube and Twitch.' },
    { 'slug': 'restaurant-menu-chooser', 'title': 'Can’t Decide What to Eat? Spin!', 'description': 'Use a wheel to pick food or restaurants.' },
    { 'slug': 'date-night-decision-wheel', 'title': 'Date Night Decision Wheel', 'description': 'Fun choices for couples and friends.' },
    { 'slug': 'classroom-behavior-rewards-wheel', 'title': 'Classroom Rewards Wheel', 'description': 'Positive reinforcement made fun.' },
    { 'slug': 'quiz-and-trivia-randomizer', 'title': 'Quiz & Trivia Randomizer', 'description': 'Randomize questions and teams.' },
    { 'slug': 'lucky-draw-and-raffle-guide', 'title': 'Lucky Draw & Raffle – Best Practices', 'description': 'Run transparent draws with our wheel.' },
    { 'slug': 'wedding-games-wheel', 'title': 'Wedding Games with a Spin', 'description': 'Entertain guests with interactive spins.' },
    { 'slug': 'festival-games-diwali-holi', 'title': 'Festival Game Ideas – Diwali to Holi', 'description': 'Family-friendly spins for celebrations.' },
    { 'slug': 'school-assembly-selector', 'title': 'School Assembly Selector', 'description': 'Pick performers or topics fairly.' },
    { 'slug': 'corporate-giveaway-ideas', 'title': 'Corporate Giveaway Ideas', 'description': 'Boost engagement at events and booths.' },
    { 'slug': 'spin-wheel-seo-benefits', 'title': 'SEO Benefits of Interactive Tools', 'description': 'Why wheels drive traffic and time-on-site.' },
    { 'slug': 'privacy-and-safety-on-cyw', 'title': 'Privacy & Safety at Custom Your Spin', 'description': 'No sign-up, no personal data required.' },
    { 'slug': 'how-to-embed-the-wheel', 'title': 'How to Embed the Wheel on Your Site', 'description': 'Simple ways to share and embed.' },
    { 'slug': 'accessibility-features', 'title': 'Accessibility Features of the Wheel', 'description': 'Keyboard support, clear colors and more.' },
]


def blog_index(request):
    return render(request, 'blog/index.html', { 'articles': ARTICLES })


def blog_article(request, slug: str):
    match = next((a for a in ARTICLES if a['slug'] == slug), None)
    if not match:
        raise Http404('Article not found')
    template_path = f"blog/{slug}.html"
    return render(request, template_path, { 'article': match, 'articles': ARTICLES })

def test_static(request):
    """Test view to check if static files are being served correctly"""
    return render(request, 'test_static.html')

# -------- Legal & Contact --------
def terms(request):
    return render(request, 'terms.html')

def contact(request):
    return render(request, 'contact.html')
