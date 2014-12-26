from django.db import models

from main.models import Club, Game


class Tip(models.Model):

    game = models.ForeignKey(Game, related_name='tips')
    club = models.ForeignKey(Club, related_name='tips')
    crowd = models.IntegerField(null=True)
    crowds_score = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)
    margin = models.IntegerField(null=True)
    margins_score = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    supercoach_score = models.IntegerField(default=0)
    winner = models.ForeignKey(Club, null=True, related_name='tip_winners')
    winners_score = models.IntegerField(default=0)

    def __str__(self):
        return '{}: {} v {}'.format(
            self.club, self.game.afl_home, self.game.afl_away)

    class Meta:
        app_label = 'main'
        ordering = ('-game', 'club')


