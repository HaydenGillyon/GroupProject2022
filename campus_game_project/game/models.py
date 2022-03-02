from django.utils import timezone
from django.db import models


class Game(models.Model):

    lobby_code = models.IntegerField()
    player_num = models.IntegerField()
    game_start_time = models.DateTimeField(default=timezone.now)
    running = models.BooleanField(default=False)

    def __str__(self):
        return str(self.lobby_code)

    def all_ready(self):
        if len(Player.objects.filter(game=self, ready=True)) == self.player_num:
            return True
        else:
            return False


class Player(models.Model):
    username = models.CharField(max_length=20)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    seeker = models.BooleanField()
    ready = models.BooleanField()
    hider_code = models.CharField(max_length=4, null=True)
    found = models.BooleanField(default=False)

    def __str__(self):
        return self.username
