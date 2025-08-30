from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Ad, Room, Player, Challenge
from django.http import HttpResponse
from django.utils import timezone
import os
import json
import uuid
from pathlib import Path

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

# Multiplayer Room Views

def create_room(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_name = data.get('name', 'Spin Challenge Room')
        max_players = data.get('max_players', 6)
        challenge_type = data.get('challenge_type', 'truth-dare')
        wheel_theme = data.get('wheel_theme', 'classic')
        
        # Create new room
        room = Room.objects.create(
            name=room_name,
            max_players=max_players,
            challenge_type=challenge_type,
            wheel_theme=wheel_theme
        )
        
        return JsonResponse({
            'success': True,
            'room_code': room.room_code,
            'room_id': room.id,
            'message': f'Room {room.room_code} created successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def join_room(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_code = data.get('room_code', '').upper()
        player_name = data.get('player_name', '')
        player_id = data.get('player_id', str(uuid.uuid4()))
        
        try:
            room = Room.objects.get(room_code=room_code, is_active=True)
            
            # Check if room is full
            if room.current_players >= room.max_players:
                return JsonResponse({
                    'success': False,
                    'message': 'Room is full!'
                })
            
            # Check if player already exists in room
            existing_player = Player.objects.filter(room=room, player_id=player_id).first()
            if existing_player:
                return JsonResponse({
                    'success': True,
                    'room_code': room.room_code,
                    'room_id': room.id,
                    'player_id': player_id,
                    'message': 'Rejoined room successfully!'
                })
            
            # Add player to room
            player = Player.objects.create(
                room=room,
                player_id=player_id,
                name=player_name
            )
            
            # Update room player count
            room.current_players = Player.objects.filter(room=room).count()
            room.last_activity = timezone.now()
            room.save()
            
            return JsonResponse({
                'success': True,
                'room_code': room.room_code,
                'room_id': room.id,
                'player_id': player_id,
                'message': f'Joined room {room.room_code} successfully!'
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found or inactive!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def get_room_status(request, room_code):
    try:
        room = Room.objects.get(room_code=room_code.upper(), is_active=True)
        players = Player.objects.filter(room=room)
        
        players_data = []
        for player in players:
            players_data.append({
                'id': player.player_id,
                'name': player.name,
                'is_ready': player.is_ready,
                'joined_at': player.joined_at.isoformat()
            })
        
        return JsonResponse({
            'success': True,
            'room': {
                'code': room.room_code,
                'name': room.name,
                'max_players': room.max_players,
                'current_players': room.current_players,
                'wheel_theme': room.wheel_theme,
                'challenge_type': room.challenge_type,
                'is_active': room.is_active
            },
            'players': players_data
        })
        
    except Room.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Room not found!'
        })

def spin_wheel(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            # Get challenge templates
            challenge_templates = {
                'truth-dare': [
                    'Tell your biggest secret',
                    'Do 10 push-ups',
                    'Sing your favorite song',
                    'Call your ex',
                    'Eat something spicy',
                    'Dance for 1 minute',
                    'Tell a funny joke',
                    'Do a cartwheel',
                    'Speak in an accent for 5 minutes',
                    'Do the worm dance'
                ],
                'this-that': [
                    'Pizza or Burger',
                    'Netflix or YouTube',
                    'Beach or Mountains',
                    'Coffee or Tea',
                    'Summer or Winter',
                    'Dogs or Cats',
                    'City or Country',
                    'Morning or Night',
                    'Sweet or Salty',
                    'Books or Movies'
                ],
                'workout': [
                    '20 Push-ups',
                    '30 Squats',
                    '1-minute Plank',
                    '20 Jumping Jacks',
                    '15 Burpees',
                    '30-second Wall Sit',
                    '20 Lunges',
                    '10 Mountain Climbers',
                    '30-second High Knees',
                    '20 Tricep Dips'
                ]
            }
            
            # Get random challenge
            import random
            challenges = challenge_templates.get(room.challenge_type, challenge_templates['truth-dare'])
            selected_challenge = random.choice(challenges)
            
            # Create challenge record
            player = Player.objects.filter(room=room, player_id=player_id).first()
            challenge = Challenge.objects.create(
                room=room,
                challenge_text=selected_challenge,
                challenge_type=room.challenge_type,
                completed_by=player
            )
            
            # Update room activity
            room.last_activity = timezone.now()
            room.save()
            
            return JsonResponse({
                'success': True,
                'challenge': selected_challenge,
                'challenge_id': challenge.id,
                'player_name': player.name if player else 'Unknown'
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def leave_room(request, room_code):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            player = Player.objects.filter(room=room, player_id=player_id).first()
            
            if player:
                player.delete()
                
                # Update room player count
                room.current_players = Player.objects.filter(room=room).count()
                room.last_activity = timezone.now()
                room.save()
                
                # If no players left, deactivate room
                if room.current_players == 0:
                    room.is_active = False
                    room.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Left room successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Player not found in room!'
                })
                
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
