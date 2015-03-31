import collections
import datetime
import itertools

from django.db import models
from django.db.models.loading import get_model

from main import constants
from main.models import Coach, Season


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

    @property
    def deadline_has_passed(self):
        return datetime.datetime.now() >= self.tipping_deadline

    @property
    def bye_clubs(self):
        """
        Find the clubs who have a bye in this round.
        """
        return [b.club for b in self.byes.order_by('club').all()]

    @property
    def has_byes(self):
        return bool(self.byes.all())

    @property
    def tipping_clubs(self):
        """
        Get the clubs that can tip in this round. They will be the clubs that
        are playing in this round. Clubs that haven't paid their fees are
        excluded.

        :return: set of clubs that can tip in this round.
        """
        fees_deadline = Round.objects.get(
            name=constants.Round.FEES_BY, season=self.season
        ).start_time

        clubs = []
        for game in self.games.all():
            clubs.extend((game.legends_away, game.legends_home))
        clubs.extend(self.bye_clubs)

        # Check if fees have been paid
        if self.start_time >= fees_deadline:
            for coach in Coach.objects.filter(season=self.season):
                if not coach.has_paid_fees:
                    if coach.club in clubs:
                        clubs.remove(coach.club)

        return set(clubs)

    @property
    def next_round(self):
        """
        Return the next round or None if round is the grand final.
        """
        if self.name == 'Grand Final':
            return None

        if self.start_time:
            rounds = Round.objects.filter(
                season=self.season, start_time__gt=self.start_time) \
                .order_by('start_time')
        else:
            rounds = Round.objects.filter(
                season=self.season, id__gt=self.id)   \
                .order_by('id')

        return rounds[0]

    @property
    def previous_round(self):
        """
        Return the previous round or None if round is Round 1
        """
        if self.name == 'Round 1':
            return None

        if self.start_time:
            rounds = Round.objects.filter(
                season=self.season, start_time__lt=self.start_time)   \
                .order_by('-start_time')
        else:
            rounds = Round.objects.filter(
                season=self.season, id__lt=self.id)   \
                .order_by('-id')

        return rounds[0]

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

    def clubs_by_games(self, games=None):
        """
        Return a list of clubs tipping in round in game order with byes last.
        """
        if games is None:
            games = self.games

        clubs = []
        for game in games:
            clubs.extend((game.legends_home, game.legends_away))

        # Add byes
        clubs.extend(self.bye_clubs)

        return clubs

    def _tips(self, games=None, key=None):
        """
        Return the tips for each game in `games` sorted by `key` (no sorting by
        default). If `games` hasn't been provided, get tips for all games in the
        round. `key` should be something like 'club' or 'game__start_time' (see
        order_by in the Django docs).
        We use raw SQL to avoid a circular import with the Tip model.
        """
        if not games:
            games = self.games.all()

        model = get_model('main', 'Tip')

        if not key:
            return model.objects.filter(game__in=games).all()
        else:
            return model.objects.filter(game__in=games).order_by(key).all()

    def tips_by_game(self, games=None):
        """
        Return a dictionary, keyed by game of the tips for each game in `games`.
        If `games` is None, get tips for all games in the round.
        If `sort_key` is given, sort tips by the order clubs appear in games
        with byes at the end.
        """
        if games is None:
            games = self.games.all()

        clubs = self.clubs_by_games(games)

        tips = {
            g: list(t) for g, t in itertools.groupby(
                self._tips(games, 'game'), key=lambda x: x.game
            )
        }

        tips_dict = collections.OrderedDict()
        for game in games:
            lookup = {t.club: t for t in tips[game]}
            tips_dict[game] = [lookup[club] for club in clubs]

        return tips_dict

    def tips_by_club(self, games=None):
        """
        Return a dictionary, keyed by club, of the tips for each of the given
        games. If games is None, get tips for all games in the round.
        """
        tips_dict = {
            c: list(t) for c, t in itertools.groupby(
                self._tips(games, 'club'), key=lambda x: x.club)
        }

        return tips_dict

    def club_tips(self, club):
        """
        Get a club's tips for this round.

        :param club: The club for which we want tips.
        :return: All of the club's tips for this round.
        """
#        return (t for t in self._tips(key='game__game_date') if t.club == club)
        return self._tips(key='game__game_date').filter(club=club)

    def club_ladders(self, club):
        """
        Get the ladders for round for club.
        Return a dictionary keyed by ladder name.
        """

        model_names = (
            'LegendsLadder', 'ColemanLadder', 'BrownlowLadder',
            'MarginsLadder', 'CrowdsLadder'
        )

        ladders = {}
        for model_name in model_names:
            name = model_name.lower()[:-6]
            model = get_model('main', model_name)
            try:
                ladders[name] = model.objects.get(round=self, club=club)
            except model.DoesNotExist:
                ladders[name] = model(round=self, club=club)

        return ladders

    def _premiership_ladders(self, name):
        """
        Return a dictionary, keyed by club, of the premiership ladders for the
        round.
        Create empty ladders if they don't exist.
        """
        model = get_model('main', name)

        ladders = model.objects.filter(round=self)

        if not ladders:
            ladders = [model(round=self, club=c) for c in self.season.clubs]

        return {l.club: l for l in ladders}

    def afl_ladders(self):
        """
        Return a dictionary, keyed by club, of the AFL ladders for the round.
        Create empty ladders if they don't exist.
        """
        return self._premiership_ladders('AFLLadder')

    def legends_ladders(self):
        """
        Return a dictionary, keyed by club, of the Legends ladders for the
        round.
        Create empty ladders if they don't exist.
        """
        return self._premiership_ladders('LegendsLadder')

    def sort_ladder(self, ladder, reverse):
        """
        Return a ladder sorted according to it's sort_order
        """

        def key_func(row):

            key = []

            for col in sort_columns:
                if col.startswith('-'):
                    key.append(-1 * getattr(row, col[1:]))
                else:
                    key.append(getattr(row, col))

            # Sort alphabetically by club if there's still a tie after all this
            if row.club.name not in sort_columns:
                key.append(row.club.name)

            return key

        sort_columns = ladder[0].sort_order

        if isinstance(sort_columns, str):
            sort_columns = [sort_columns]

        return sorted(ladder, key=key_func, reverse=reverse)

    def get_streak_ladders(self):
        """
        Return the streak ladders for the round.

        Create empty ladders if they don't exist.
        """
        model = get_model('main', 'StreakLadder')

        ladders = model.objects.filter(round=self)

        if not ladders:
            ladders = [model(round=self, club=c) for c in self.season.clubs]

        return {l.club: l for l in ladders}
