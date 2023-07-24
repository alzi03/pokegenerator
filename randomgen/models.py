from django.db import models

# Create your models here.

class GuessStreak(models.Model):
    
    streak = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default='')