from django.db import models

from main.models import Game, Player


class Vote(models.Model):

    game = models.ForeignKey(Game, related_name='votes')
    player = models.ForeignKey(Player, related_name='votes')
    votes = models.IntegerField()

    class Meta:
        app_label = 'main'

    def __str__(self):

        return '{} - {} {} votes'.format(self.game, self.player, self.votes)

