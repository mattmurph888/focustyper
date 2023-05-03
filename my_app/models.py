from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Level(models.Model):
    level_number = models.IntegerField(unique=True, default=None)
    level_title = models.CharField(max_length=50)
    level_text = models.CharField(max_length=500)

    def __str__(self) -> str:
        return f'Level {self.level_number}: {self.level_title}'
    

class User_Level_Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, default=None)
    accuracy = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username}'s {self.level.level_title} record"