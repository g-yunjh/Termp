from django.db import models

class FlashCard(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=100)
    difficulty = models.IntegerField(default=0)
    rounds_seen = models.JSONField(default=dict)