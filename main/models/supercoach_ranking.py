from django.db import models

from main.models import Game, Player


class SupercoachRanking(models.Model):
    """
    Supercoach rankings for top 5 scores.

    Top score gets 5, second gets 4 and so on until everyone who doesn't get a
    top 5 (or 6 or 7 or... depending on ties) score gets a zero ranking.

    """
    game = models.ForeignKey(Game, related_name='supercoach_rankings')
    player = models.ForeignKey(Player, related_name='supercoach_rankings')
    ranking = models.IntegerField()

    class Meta:
        app_label = 'main'
        db_table = 'main_supercoach_ranking'

    def __str__(self):

        return '{} - {} {} votes'.format(self.game, self.player, self.ranking)

