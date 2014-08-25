from django.db import models

from main.models import Player, Tip


class VoteTip(models.Model):

    player = models.ForeignKey(Player, related_name='vote_tips', null=True)
    tip = models.ForeignKey(Tip, related_name='vote_tips')

    class Meta:
        app_label = 'main'
        ordering = (
            'player__last_name', 'player__initial', 'player__first_name')

    def __str__(self):
        return str(self.player)
