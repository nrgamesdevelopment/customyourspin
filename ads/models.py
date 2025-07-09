from django.db import models

# Create your models here.

class Ad(models.Model):
    ad_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ads/')
    link = models.URLField()

    def __str__(self):
        return self.ad_name
