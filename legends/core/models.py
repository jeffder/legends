from django.contrib.auth.models import User
from django.db import models


class Season(models.Model):

    season = models.IntegerField(null=False)

    # Every season from 2008 has full data (coaches, games, tips, results,
    # ladders etc). The rest have some ladders and category winners except
    # 2006...
    has_full_data = models.BooleanField(default=True)

    # ...which has no data except the Premier.
    has_no_data = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.season)

    class Meta:
        ordering = ['-season']


class Club(models.Model):

    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    user = models.ForeignKey(User, unique=True, related_name='clubs')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Coach(models.Model):

    club = models.ForeignKey(Club, related_name='coaches')
    first_name = models.CharField(max_length=30, null=True)
    has_paid_fees = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    last_name = models.CharField(max_length=30, null=True)
    season = models.ForeignKey(Season, related_name='coaches')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'coaches'
        ordering = ['-season', 'club', 'last_name', 'first_name']

    @property
    def name(self):
        '''
        Return the coach's full name as first_name last_name.
        '''
        return '{} {}'.format(self.first_name, self.last_name)


class Player(models.Model):

    club = models.ForeignKey(Club, related_name='players')
    first_name = models.CharField(max_length=30)
    initial = models.CharField(max_length=1, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    season = models.ForeignKey(Season, related_name='players')
    supercoach_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.club.nickname)

    class Meta:
        ordering = ['-season', 'club', 'last_name', 'initial', 'first_name']

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

    def __str__(self):
        return '{} {}'.format(self.season, self.name)

    class Meta:
        ordering = ('-season', 'start_time')


class Ground(models.Model):

    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

