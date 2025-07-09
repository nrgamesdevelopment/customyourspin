from django.shortcuts import render
from django.http import JsonResponse
from .models import Ad

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
