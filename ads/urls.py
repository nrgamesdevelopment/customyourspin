from django.urls import path
from .views import latest_ad, all_ads, blog_index, blog_article, test_static, terms, contact

urlpatterns = [
    path('latest/', latest_ad, name='latest_ad'),
    path('all/', all_ads, name='all_ads'),
    # Blog
    path('blog/', blog_index, name='blog_index'),
    path('blog/<slug:slug>/', blog_article, name='blog_article'),
    # Legal & Contact
    path('terms/', terms, name='terms'),
    path('contact/', contact, name='contact'),
    # Test static files
    path('test-static/', test_static, name='test_static'),
] 