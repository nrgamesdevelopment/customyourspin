"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ads.views import home
from django.contrib.sitemaps.views import sitemap
from ads.sitemaps import StaticViewSitemap
from django.http import HttpResponse
from django.conf import settings
import os

sitemaps = {
    'static': StaticViewSitemap,
}

def ads_txt(request):
    """Serve the ads.txt file"""
    ads_txt_path = os.path.join(settings.BASE_DIR, 'ads.txt')
    try:
        with open(ads_txt_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse('File not found', status=404)

def robots_txt(request):
    """Serve the robots.txt file"""
    robots_txt_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    try:
        with open(robots_txt_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        return HttpResponse('User-agent: *\nAllow: /', content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('ads/', include('ads.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('ads.txt', ads_txt, name='ads_txt'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
