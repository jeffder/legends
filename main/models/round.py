from django.contrib.auth.models import User
from django.db import models

from main.models import Season


class Round(models.Model):

    _status_choices = (
        ('Final', 'Final'),
        ('Provisional', 'Provisional'),
        ('Scheduled', 'Scheduled')
    )
    _status_help_text = ''.join(
        (
            'Round status:\n',
            '\tscheduled to be played\n',
            '\tprovisional\n',
            '\tall games are completed.'
        )
    )

    is_finals = models.BooleanField(default=False)
    name = models.CharField(max_length=20)
    num_bogs = models.IntegerField()
    num_games = models.IntegerField()
    season = models.ForeignKey(Season, related_name='rounds')
    status = models.CharField(
        max_length=15,
        choices=_status_choices,
        help_text=_status_help_text
    )
    start_time = models.DateTimeField(null=True)
    tipping_deadline = models.DateTimeField(null=True)

    class Meta:
        ordering = ('-season', 'start_time')

    def __str__(self):
        return '{} {}'.format(self.season, self.name)
