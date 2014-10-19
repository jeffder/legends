from django.db import models

from main.models import Player, Round


class Supercoach(models.Model):
    '''
    Supercoach scores
    '''

    round = models.ForeignKey(Round, related_name='supercoaches')
    player = models.ForeignKey(Player, related_name='supercoaches')
    score = models.IntegerField()

    class Meta:
        app_label = 'main'
        ordering = ('-round__season', 'round__start_time', 'player')
        verbose_name_plural = 'supercoaches'
