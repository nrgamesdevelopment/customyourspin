from django.db import models
from django.utils import timezone

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
