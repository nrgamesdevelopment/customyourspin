from django.urls import path
from .views import latest_ad, all_ads

urlpatterns = [
    path('latest/', latest_ad, name='latest_ad'),
    path('all/', all_ads, name='all_ads'),
] 