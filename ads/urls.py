from django.urls import path
from .views import latest_ad, all_ads, create_room, join_room, get_room_status, spin_wheel, leave_room

urlpatterns = [
    path('latest/', latest_ad, name='latest_ad'),
    path('all/', all_ads, name='all_ads'),
    
    # Multiplayer Room URLs
    path('room/create/', create_room, name='create_room'),
    path('room/join/', join_room, name='join_room'),
    path('room/<str:room_code>/status/', get_room_status, name='get_room_status'),
    path('room/<str:room_code>/spin/', spin_wheel, name='spin_wheel'),
    path('room/<str:room_code>/leave/', leave_room, name='leave_room'),
] 