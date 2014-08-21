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

    class Meta:
        ordering = ['-season']

    def __str__(self):
        return '{}'.format(self.season)


class Club(models.Model):

    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    user = models.ForeignKey(User, unique=True, related_name='clubs')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Coach(models.Model):

    club = models.ForeignKey(Club, related_name='coaches')
    first_name = models.CharField(max_length=30, null=True)
    has_paid_fees = models.BooleanField(default=False)
    is_assistant = models.BooleanField(default=False)
    last_name = models.CharField(max_length=30, null=True)
    season = models.ForeignKey(Season, related_name='coaches')

    class Meta:
        verbose_name_plural = 'coaches'
        ordering = ['-season', 'club', 'last_name', 'first_name']

    def __str__(self):
        return self.name

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

    class Meta:
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


class Ground(models.Model):

    name = models.CharField(max_length=20, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Game(models.Model):
    '''
    AFL/Legends games
    '''

    _statusChoices = (
        ('Final', 'Final'),
        ('Provisional', 'Provisional'),
        ('Scheduled', 'Scheduled')
    )
    _status_help_text = (
        'Game status:\n'
        '\tFinal - game has been completed\n'
        '\tProvisional - game has a provisional result\n'
        '\tScheduled - game has not been completed\n'
    )

    crowd = models.IntegerField(default=0)
    finals_game = models.IntegerField(
        blank=True,
        null=True,
        help_text='Number of game in finals (1-9)'
    )
    game_date = models.DateTimeField(null=True, blank=True)
    round = models.ForeignKey(Round, related_name='games')
    status = models.CharField(
        max_length=15,
        choices=_statusChoices,
        help_text=_status_help_text
    )
    tipping_deadline = models.DateTimeField(null=True, blank=True)
    ground = models.ForeignKey(Ground, related_name='games')

    # AFL specific fields
    afl_away = models.ForeignKey(Club, related_name='afl_game_away')
    afl_away_score = models.IntegerField(default=0)
    afl_home = models.ForeignKey(Club, related_name='afl_game_home')
    afl_home_score = models.IntegerField(default=0)

    # Legends specific fields
    legends_away = models.ForeignKey(Club, related_name='legends_game_away')
    legends_away_score = models.IntegerField(default=0)
    legends_away_winners_bonus = models.IntegerField(default=0)
    legends_home = models.ForeignKey(Club, related_name='legends_game_home')
    legends_home_score = models.IntegerField(default=0)
    legends_home_winners_bonus = models.IntegerField(default=0)

    class Meta:
        ordering = ('-round__season', 'round', 'game_date', 'afl_home')

    def __str__(self):
        return u'%s: %s v %s' % (self.round, self.afl_home, self.afl_away)

