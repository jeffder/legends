from django.db import models

from main.models import Player, Tip


class SupercoachTip(models.Model):

    player = models.ForeignKey(
        Player, related_name='supercoach_tips', null=True)
    tip = models.ForeignKey(Tip, related_name='supercoach_tips')

    class Meta:
        app_label = 'main'
        db_table = 'main_supercoach_tip'
        ordering = (
            'player__last_name', 'player__initial', 'player__first_name')

    def __str__(self):
        return str(self.player)
