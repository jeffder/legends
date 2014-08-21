from django.db import models

from main.models import Club, Season


class Coach(models.Model):

    club = models.ForeignKey(Club, related_name='coaches')
    first_name = models.CharField(max_length=30, null=True)
    has_paid_fees = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    last_name = models.CharField(max_length=30, null=True)
    season = models.ForeignKey(Season, related_name='coaches')

    class Meta:
        app_label = 'main'
        ordering = ['-season', 'club', 'last_name', 'first_name']
        verbose_name_plural = 'coaches'

    def __str__(self):
        return self.name

    @property
    def name(self):
        '''
        Return the coach's full name as first_name last_name.
        '''
        return '{} {}'.format(self.first_name, self.last_name)
