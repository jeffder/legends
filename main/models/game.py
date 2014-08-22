from django.db import models

from main.models import Club, Ground, Round


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
    legends_away_crowds_score = models.IntegerField(default=0, verbose_name='Crowds')
    legends_away_margins_score = models.IntegerField(default=0, verbose_name='Margins')
    legends_away_score = models.IntegerField(default=0, verbose_name='Total')
    legends_away_votes_score = models.IntegerField(default=0, verbose_name='Votes')
    legends_away_winners_bonus = models.IntegerField(default=0, verbose_name='Winners Bonus')
    legends_away_winners_score = models.IntegerField(default=0, verbose_name='Winners')
    legends_home = models.ForeignKey(Club, related_name='legends_game_home')
    legends_home_crowds_score = models.IntegerField(default=0, verbose_name='Crowds')
    legends_home_margins_score = models.IntegerField(default=0, verbose_name='Margins')
    legends_home_score = models.IntegerField(default=0, verbose_name='Total')
    legends_home_votes_score = models.IntegerField(default=0, verbose_name='Votes')
    legends_home_winners_bonus = models.IntegerField(default=0, verbose_name='Winners Bonus')
    legends_home_winners_score = models.IntegerField(default=0, verbose_name='Winners')

    class Meta:
        app_label = 'main'
        ordering = ('-round__season', 'round', 'game_date', 'afl_home')

    def __str__(self):
        return u'%s: %s v %s' % (self.round, self.afl_home, self.afl_away)
