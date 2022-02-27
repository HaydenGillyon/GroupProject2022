from django.db import models

class Game(models.Model):
    lobby_code = models.IntegerField()
    player_num = models.IntegerField()

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

    def __str__(self):
        return self.username

