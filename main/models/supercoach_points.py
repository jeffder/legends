from django.db import models

from main.models import Player, Round


class SupercoachPoints(models.Model):
    '''
    Actual supercoach scores
    '''

    round = models.ForeignKey(Round, related_name='supercoach_points')
    player = models.ForeignKey(Player, related_name='supercoach_points')
    score = models.IntegerField()

    class Meta:
        app_label = 'main'
        db_table = 'main_supercoach_points'
        ordering = ('-round__season', 'round__start_time', 'player')
        verbose_name_plural = 'supercoach_points'
