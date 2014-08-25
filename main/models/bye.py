from django.db import models

from main.models import Club, Round


class Bye(models.Model):
    '''
    Bye games
    '''

    club = models.ForeignKey(Club, related_name='byes')
    crowds_score = models.IntegerField(default=0)
    margins_score = models.IntegerField(default=0)
    round = models.ForeignKey(Round, related_name='byes')
    score = models.IntegerField(default=0)
    votes_score = models.IntegerField(default=0)
    winners_bonus = models.IntegerField(default=0)
    winners_score = models.IntegerField(default=0)

    class Meta:
        app_label = 'main'
        ordering = ('-round__season', 'round', 'club')

    def __str__(self):
        return '{} {}'.format(self.round, self.club)
