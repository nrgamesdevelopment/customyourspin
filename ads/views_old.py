from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Ad, Room, Player, Challenge, GameRound
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
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

@csrf_exempt
def create_room(request):
    if request.method == 'POST':
        try:
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
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'message': f'Error creating room: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def start_game(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            # Check if player is room owner
            player = Player.objects.filter(room=room, player_id=player_id, is_room_owner=True).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Only room owner can start the game!'
                })
            
            # Check if enough players
            if room.current_players < 2:
                return JsonResponse({
                    'success': False,
                    'message': 'Need at least 2 players to start!'
                })
            
            # Start the game
            room.game_started = True
            room.current_turn = 0
            room.current_round = 1
            room.save()
            
            # Create first round
            players = Player.objects.filter(room=room).order_by('turn_order')
            first_player = players.first()
            
            GameRound.objects.create(
                room=room,
                round_number=1,
                current_player=first_player
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Game started!',
                'current_player': first_player.name,
                'round': 1
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def add_custom_challenge(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            challenge_text = data.get('challenge_text', '').strip()
            
            if not challenge_text:
                return JsonResponse({
                    'success': False,
                    'message': 'Challenge text cannot be empty!'
                })
            
            player = Player.objects.filter(room=room, player_id=player_id).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Player not found in room!'
                })
            
            # Create custom challenge
            challenge = Challenge.objects.create(
                room=room,
                challenge_text=challenge_text,
                challenge_type=room.challenge_type,
                created_by=player,
                is_custom=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Custom challenge added!',
                'challenge_id': challenge.id
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def next_turn(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            if not room.game_started:
                return JsonResponse({
                    'success': False,
                    'message': 'Game not started yet!'
                })
            
            # Get current player
            players = Player.objects.filter(room=room).order_by('turn_order')
            current_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            # Check if it's the current player's turn
            if current_player.player_id != player_id:
                return JsonResponse({
                    'success': False,
                    'message': f"It's {current_player.name}'s turn!"
                })
            
            # Move to next turn
            room.current_turn = (room.current_turn + 1) % len(players)
            
            # Check if round is complete
            if room.current_turn == 0:
                room.current_round += 1
                if room.current_round > room.total_rounds:
                    # Game finished
                    room.game_started = False
                    room.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Game completed!',
                        'game_finished': True
                    })
            
            room.save()
            
            # Get next player
            next_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            return JsonResponse({
                'success': True,
                'message': f'Turn passed to {next_player.name}',
                'current_player': next_player.name,
                'current_turn': room.current_turn,
                'round': room.current_round
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
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
                name=player_name,
                turn_order=room.current_players,  # Set turn order
                is_room_owner=(room.current_players == 0)  # First player is room owner
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

@csrf_exempt
def start_game(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            # Check if player is room owner
            player = Player.objects.filter(room=room, player_id=player_id, is_room_owner=True).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Only room owner can start the game!'
                })
            
            # Check if enough players
            if room.current_players < 2:
                return JsonResponse({
                    'success': False,
                    'message': 'Need at least 2 players to start!'
                })
            
            # Start the game
            room.game_started = True
            room.current_turn = 0
            room.current_round = 1
            room.save()
            
            # Create first round
            players = Player.objects.filter(room=room).order_by('turn_order')
            first_player = players.first()
            
            GameRound.objects.create(
                room=room,
                round_number=1,
                current_player=first_player
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Game started!',
                'current_player': first_player.name,
                'round': 1
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def add_custom_challenge(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            challenge_text = data.get('challenge_text', '').strip()
            
            if not challenge_text:
                return JsonResponse({
                    'success': False,
                    'message': 'Challenge text cannot be empty!'
                })
            
            player = Player.objects.filter(room=room, player_id=player_id).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Player not found in room!'
                })
            
            # Create custom challenge
            challenge = Challenge.objects.create(
                room=room,
                challenge_text=challenge_text,
                challenge_type=room.challenge_type,
                created_by=player,
                is_custom=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Custom challenge added!',
                'challenge_id': challenge.id
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def next_turn(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            if not room.game_started:
                return JsonResponse({
                    'success': False,
                    'message': 'Game not started yet!'
                })
            
            # Get current player
            players = Player.objects.filter(room=room).order_by('turn_order')
            current_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            # Check if it's the current player's turn
            if current_player.player_id != player_id:
                return JsonResponse({
                    'success': False,
                    'message': f"It's {current_player.name}'s turn!"
                })
            
            # Move to next turn
            room.current_turn = (room.current_turn + 1) % len(players)
            
            # Check if round is complete
            if room.current_turn == 0:
                room.current_round += 1
                if room.current_round > room.total_rounds:
                    # Game finished
                    room.game_started = False
                    room.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Game completed!',
                        'game_finished': True
                    })
            
            room.save()
            
            # Get next player
            next_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            return JsonResponse({
                'success': True,
                'message': f'Turn passed to {next_player.name}',
                'current_player': next_player.name,
                'current_turn': room.current_turn,
                'round': room.current_round
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
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

@csrf_exempt
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

@csrf_exempt
def start_game(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            # Check if player is room owner
            player = Player.objects.filter(room=room, player_id=player_id, is_room_owner=True).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Only room owner can start the game!'
                })
            
            # Check if enough players
            if room.current_players < 2:
                return JsonResponse({
                    'success': False,
                    'message': 'Need at least 2 players to start!'
                })
            
            # Start the game
            room.game_started = True
            room.current_turn = 0
            room.current_round = 1
            room.save()
            
            # Create first round
            players = Player.objects.filter(room=room).order_by('turn_order')
            first_player = players.first()
            
            GameRound.objects.create(
                room=room,
                round_number=1,
                current_player=first_player
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Game started!',
                'current_player': first_player.name,
                'round': 1
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def add_custom_challenge(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            challenge_text = data.get('challenge_text', '').strip()
            
            if not challenge_text:
                return JsonResponse({
                    'success': False,
                    'message': 'Challenge text cannot be empty!'
                })
            
            player = Player.objects.filter(room=room, player_id=player_id).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Player not found in room!'
                })
            
            # Create custom challenge
            challenge = Challenge.objects.create(
                room=room,
                challenge_text=challenge_text,
                challenge_type=room.challenge_type,
                created_by=player,
                is_custom=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Custom challenge added!',
                'challenge_id': challenge.id
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def next_turn(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            if not room.game_started:
                return JsonResponse({
                    'success': False,
                    'message': 'Game not started yet!'
                })
            
            # Get current player
            players = Player.objects.filter(room=room).order_by('turn_order')
            current_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            # Check if it's the current player's turn
            if current_player.player_id != player_id:
                return JsonResponse({
                    'success': False,
                    'message': f"It's {current_player.name}'s turn!"
                })
            
            # Move to next turn
            room.current_turn = (room.current_turn + 1) % len(players)
            
            # Check if round is complete
            if room.current_turn == 0:
                room.current_round += 1
                if room.current_round > room.total_rounds:
                    # Game finished
                    room.game_started = False
                    room.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Game completed!',
                        'game_finished': True
                    })
            
            room.save()
            
            # Get next player
            next_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            return JsonResponse({
                'success': True,
                'message': f'Turn passed to {next_player.name}',
                'current_player': next_player.name,
                'current_turn': room.current_turn,
                'round': room.current_round
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
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

@csrf_exempt
def start_game(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            # Check if player is room owner
            player = Player.objects.filter(room=room, player_id=player_id, is_room_owner=True).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Only room owner can start the game!'
                })
            
            # Check if enough players
            if room.current_players < 2:
                return JsonResponse({
                    'success': False,
                    'message': 'Need at least 2 players to start!'
                })
            
            # Start the game
            room.game_started = True
            room.current_turn = 0
            room.current_round = 1
            room.save()
            
            # Create first round
            players = Player.objects.filter(room=room).order_by('turn_order')
            first_player = players.first()
            
            GameRound.objects.create(
                room=room,
                round_number=1,
                current_player=first_player
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Game started!',
                'current_player': first_player.name,
                'round': 1
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def add_custom_challenge(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            challenge_text = data.get('challenge_text', '').strip()
            
            if not challenge_text:
                return JsonResponse({
                    'success': False,
                    'message': 'Challenge text cannot be empty!'
                })
            
            player = Player.objects.filter(room=room, player_id=player_id).first()
            if not player:
                return JsonResponse({
                    'success': False,
                    'message': 'Player not found in room!'
                })
            
            # Create custom challenge
            challenge = Challenge.objects.create(
                room=room,
                challenge_text=challenge_text,
                challenge_type=room.challenge_type,
                created_by=player,
                is_custom=True
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Custom challenge added!',
                'challenge_id': challenge.id
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def next_turn(request, room_code):
    if request.method == 'POST':
        try:
            room = Room.objects.get(room_code=room_code.upper(), is_active=True)
            data = json.loads(request.body)
            player_id = data.get('player_id')
            
            if not room.game_started:
                return JsonResponse({
                    'success': False,
                    'message': 'Game not started yet!'
                })
            
            # Get current player
            players = Player.objects.filter(room=room).order_by('turn_order')
            current_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            # Check if it's the current player's turn
            if current_player.player_id != player_id:
                return JsonResponse({
                    'success': False,
                    'message': f"It's {current_player.name}'s turn!"
                })
            
            # Move to next turn
            room.current_turn = (room.current_turn + 1) % len(players)
            
            # Check if round is complete
            if room.current_turn == 0:
                room.current_round += 1
                if room.current_round > room.total_rounds:
                    # Game finished
                    room.game_started = False
                    room.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'Game completed!',
                        'game_finished': True
                    })
            
            room.save()
            
            # Get next player
            next_player = players[room.current_turn] if room.current_turn < len(players) else players[0]
            
            return JsonResponse({
                'success': True,
                'message': f'Turn passed to {next_player.name}',
                'current_player': next_player.name,
                'current_turn': room.current_turn,
                'round': room.current_round
            })
            
        except Room.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Room not found!'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
