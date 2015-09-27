import datetime

from django.db import models

from main.models import Club, Ground, Round


class Game(models.Model):
    """
    AFL/Legends games
    """

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
    is_manual_result = models.BooleanField(default=False)

    # AFL specific fields
    afl_away = models.ForeignKey(Club, related_name='afl_game_away')
    afl_away_score = models.IntegerField(default=0)
    afl_home = models.ForeignKey(Club, related_name='afl_game_home')
    afl_home_score = models.IntegerField(default=0)

    # Legends specific fields
    legends_away = models.ForeignKey(Club, related_name='legends_game_away')
    legends_away_crowds_score = models.IntegerField(
        default=0, verbose_name='Away Crowds')
    legends_away_margins_score = models.IntegerField(
        default=0, verbose_name='Away Margins')
    legends_away_score = models.IntegerField(
        default=0, verbose_name='Away Total')
    legends_away_supercoach_score = models.IntegerField(
        default=0, verbose_name='Away Supercoach Scores')
    legends_away_winners_bonus = models.IntegerField(
        default=0, verbose_name='Away Winners Bonus')
    legends_away_winners_score = models.IntegerField(
        default=0, verbose_name='Away Winners')
    legends_home = models.ForeignKey(Club, related_name='legends_game_home')
    legends_home_crowds_score = models.IntegerField(
        default=0, verbose_name='Home Crowds')
    legends_home_margins_score = models.IntegerField(
        default=0, verbose_name='Home Margins')
    legends_home_score = models.IntegerField(
        default=0, verbose_name='Home Total')
    legends_home_supercoach_score = models.IntegerField(
        default=0, verbose_name='Home Supercoach Scores')
    legends_home_winners_bonus = models.IntegerField(
        default=0, verbose_name='Home Winners Bonus')
    legends_home_winners_score = models.IntegerField(
        default=0, verbose_name='Home Winners')

    class Meta:
        app_label = 'main'
        ordering = ('-round__season', 'round', 'game_date', 'afl_home')

    def __str__(self):
        return u'%s: %s v %s' % (self.round, self.afl_home, self.afl_away)

    @property
    def deadline_has_passed(self):
        """
        Determine if the tipping deadline has passed.

        The last home/away round is a floating round and will have no dates and
        times for its fixtures until after the previous round has been played.
        So, it won't have a tipping deadline until then.
        """
        try:
            return datetime.datetime.now() >= self.tipping_deadline
        except TypeError:
            return False

    def initialise_legends_scores(self):
        """
        Initialise legends scores
        """
        score_types = (
            'crowds_score', 'margins_score', 'score',
            'supercoach_score', 'winners_bonus', 'winners_score'
        )

        for team in ('away', 'home'):
            for score_type in score_types:
                attr = 'legends_{}_{}'.format(team, score_type)
                setattr(self, attr, 0)

    def _winner(self, kind):
        away = getattr(self, '{}_away'.format(kind))
        away_score = getattr(self, '{}_away_score'.format(kind))
        home = getattr(self, '{}_home'.format(kind))
        home_score = getattr(self, '{}_home_score'.format(kind))

        if home_score > away_score:
            return home
        elif home_score < away_score:
            return away
        elif self.round.is_finals:
            # If a finals game is a draw, the higher placed team on the ladder
            # is declared the winner. This will be the home team.
            return home
        else:
            return None

    @property
    def afl_winner(self):
        return self._winner('afl')

    @property
    def legends_winner(self):
        return self._winner('legends')

    def _loser(self, kind):
        away = getattr(self, '{}_away'.format(kind))
        away_score = getattr(self, '{}_away_score'.format(kind))
        home = getattr(self, '{}_home'.format(kind))
        home_score = getattr(self, '{}_home_score'.format(kind))

        if home_score > away_score:
            return away
        elif home_score < away_score:
            return home
        else:
            return None

    @property
    def afl_loser(self):
        return self._loser('afl')

    @property
    def legends_loser(self):
        return self._loser('legends')

    @property
    def margin(self):
        return abs(self.afl_home_score - self.afl_away_score)

    def tips_by_club(self, clubs):
        """
        Get the tips for the game sorted by the order of clubs in clubs.

        :param clubs:
            A list or other iterable with an index attribute used to sort the
            tips.
        :return:
            A sorted list of tips
        """
        if not self.tips.all():
            self.create_tips()

        tips = sorted(self.tips.all(), key=lambda x: clubs.index(x.club))

        return tips

    def is_legends_home_club(self, club):
        """
        Is the club the legends home team?
        """
        return club == self.legends_home

    def create_tips(self):
        """
        Create default tips for this game.
        """
        clubs = self.round.tipping_clubs
        num_sc = self.round.num_bogs

        tip_model = models.loading.get_model('main', 'Tip')
        sc_tip_model = models.loading.get_model('main', 'SupercoachTip')

        for club in clubs:
            args = {
                'game': self,
                'club': club,
                'crowd': None,
                'is_default': True,
                'margin': None,
                'winner': None
            }
            tip = tip_model(**args)
            tip.save()

            for i in range(num_sc):
                args = {
                    'player': None,
                    'tip': tip
                }
                sc_tip = sc_tip_model(**args)
                sc_tip.save()
