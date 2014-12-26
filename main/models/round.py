import collections
import datetime
import itertools

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
        app_label = 'main'
        ordering = ('-season', 'start_time')

    def __str__(self):
        return '{} {}'.format(self.season, self.name)

    @property
    def tab_label(self):
        """
        Create a label for tabs in the round nav.
        """
        if self.name == 'Grand Final':
            return 'GF'

        num = self.name.split()[-1]

        if self.name.startswith('Round'):
            return num
        else:
            return 'F%s' % num

    def set_tipping_deadline(self):
        """
        Set the tipping deadline for the round. The deadline will change if the
        round is split or has games played other than on a Friday, Saturday or
        Sunday.
        """
        for game in self.games.all():
            if game.status == 'Scheduled':
                if not game.deadline_has_passed:
                    self.tipping_deadline = game.tipping_deadline
                    break

    @property
    def deadline_has_passed(self):
        return datetime.datetime.now() >= self.tipping_deadline

    def round_started(self):
        """
        Has the round started yet?
        """
        return self.start_time <= datetime.datetime.now()

    def clubs_by_games(self, games=None):
        """
        Return a list of clubs tipping in round in home/away game order with
        byes at the end.
        """
        if games is None:
            games = self.games

        clubs = []
        for game in games:
            clubs.extend((game.legends_home, game.legends_away))

        # Add byes
        clubs.extend(self.bye_clubs)

        return clubs

    def tips(self, games=None, sort_by_game=False):
        """
        Return a dictionary, keyed by game, of the tips for each of the given
        games. If games is None, get tips for all games in the round.
        If sort_by_game is True, sort tips by the order clubs appear in games
        with byes at the end.
        """
        if sort_by_game:
            clubs = self.clubs_by_games(games)

        tips_dict = collections.OrderedDict()
        for game in games:
            if sort_by_game:
                lookup = {t.club: t for t in game.tips.all()}
                tips_dict[game] = [lookup[club] for club in clubs]
            else:
                tips_dict[game] = game.tips.all()

        return tips_dict

    @property
    def bye_clubs(self):
        """
        Find the clubs who have a bye in this round.
        """
        return [b.club for b in self.byes.all().order_by('club')]

    @property
    def has_byes(self):
        return bool(self.byes.all())