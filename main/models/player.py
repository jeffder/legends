from django.db import models

from main.models import Club, Season


class Player(models.Model):

    club = models.ForeignKey(Club, related_name='players')
    first_name = models.CharField(max_length=30)
    initial = models.CharField(max_length=1, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    season = models.ForeignKey(Season, related_name='players')
    supercoach_name = models.CharField(max_length=30, null=True)

    class Meta:
        app_label = 'main'
        ordering = ['-season', 'club', 'last_name', 'initial', 'first_name']

    def __str__(self):
        return '{} ({})'.format(self.name, self.club.nickname)

    @property
    def name(self):
        '''
        Return the player's full name as first_name initial last_name.
        '''
        if self.initial:
            return '{} {}. {}'.format(
                self.first_name, self.initial, self.last_name)
        else:
            return '{} {}'.format(self.first_name, self.last_name)
