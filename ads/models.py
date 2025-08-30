from django.db import models
from django.utils import timezone
import uuid
import json

# Create your models here.

class Ad(models.Model):
    ad_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ads/')
    link = models.URLField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.ad_name
    
    class Meta:
        ordering = ['-created_at']

def generate_room_code():
    return str(uuid.uuid4())[:6].upper()

class Room(models.Model):
    room_code = models.CharField(max_length=6, unique=True, default=generate_room_code)
    name = models.CharField(max_length=100, default="Spin Challenge Room")
    max_players = models.IntegerField(default=6)
    current_players = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)
    
    # Room settings
    wheel_theme = models.CharField(max_length=20, default='classic')
    challenge_type = models.CharField(max_length=50, default='truth-dare')
    
    def __str__(self):
        return f"Room {self.room_code} - {self.current_players}/{self.max_players} players"
    
    class Meta:
        ordering = ['-last_activity']

class Player(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='players')
    player_id = models.CharField(max_length=100)  # Session ID or user identifier
    name = models.CharField(max_length=50)
    is_ready = models.BooleanField(default=False)
    joined_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.name} in {self.room.room_code}"
    
    class Meta:
        ordering = ['joined_at']

class Challenge(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='challenges')
    challenge_text = models.TextField()
    challenge_type = models.CharField(max_length=50)
    is_completed = models.BooleanField(default=False)
    completed_by = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Challenge: {self.challenge_text[:50]}..."
    
    class Meta:
        ordering = ['-created_at']
