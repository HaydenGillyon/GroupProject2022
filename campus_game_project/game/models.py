from django.db import models
from welcome.models import User


class Game(models.Model):

    lobby_code = models.IntegerField()
    player_num = models.IntegerField()
    players_finished = models.IntegerField(default=0)
    game_start_time = models.FloatField(default=0)
    running = models.BooleanField(default=False)
    winner = models.CharField(max_length=20, default='N')
    hiding_time = models.IntegerField(default=60)
    seeking_time = models.IntegerField(default=600)
    seeker_num = models.IntegerField(default=1)
    radius = models.IntegerField(default=100)
    lobby_longitude = models.FloatField(default=0.0)
    lobby_latitude = models.FloatField(default=0.0)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    seeker = models.BooleanField()
    ready = models.BooleanField()
    hider_code = models.CharField(max_length=4, null=True)
    found = models.BooleanField(default=False)

    def __str__(self):
        return self.username
