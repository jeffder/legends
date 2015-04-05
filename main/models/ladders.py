from django.db import models

from main import constants
from main.models import Club, Round


class BaseLadder(models.Model):
    """
    Base class for ladders
    """

    club = models.ForeignKey(Club, related_name='%(class)ss')
    position = models.IntegerField(default=0, null=False)
    previous_position = models.IntegerField(default=0, null=False)
    round = models.ForeignKey(Round, related_name='%(class)ss')

    class Meta:
        abstract = True

    def __add__(self, other=None):
        """
        Return a ladder instance containing the "sum" of two ladders.

        The other argument must be an instance of self's class or None, in
        which case it is assumed that round is Round 1.

        All fields except id, club and round and the aggregate fields are
        added. Aggregate fields are recalculated.

        If a field exists in self but not in other, add zero.

        There is no need to do anything for the position, and points fields.
        """
        # Error checking
        if other is None:
            return self

        if not isinstance(other, self.__class__):
            raise TypeError(
                'Other ladder (%s) must be an instance of %s.'
                % (other.__class__, self.__class__)
            )

        if self.round == other.round:
            raise ValueError(
                'Cannot add ladders for the same round (%s)'
                % self.round
            )

        if not self.club == other.club:
            raise ValueError(
                'Cannot add ladders for different clubs (%s and %s)'
                % (self.club, other.club)
            )

        # Add the other ladder if there is one
        if other is not None:
            excluded = ['id', 'club', 'round']
            excluded.extend(self.aggregate_fields)
            add_fields = [
                f.name for f in self._meta.fields if f.name not in excluded
            ]

            for field in add_fields:
                setattr(
                    self,
                    field,
                    getattr(self, field) + getattr(other, field, 0))

            # Set previous position
            self.previous_position = other.position

        if self.is_premiership:
            self.calculate_played()
            self.calculate_percentage()
#            self.round.season.club_games_played(self.club)
            self.calculate_premiership_points()

        if self.has_strike_rate:
            self.calculate_strike_rates()

        # Calculate the aggregate values
        if self.has_min_max_for_against:
            self.calculate_min_max_scores()
            self.calculate_average_scores()

        return self

    def clear(self):

        excluded = ['id', 'club', 'round']
        for f in [f.name for f in self._meta.fields if f.name not in excluded]:
            setattr(self, f, 0)

    def update_columns(self, tip):
        """
        Update columns in a premiership ladder
        """
        raise NotImplementedError(
            'ERROR: update_columns() must be implemented in a subclass of {}.'
            .format(self.__class__.__name__)
        )

    def finalise(self):
        """
        Add the previous ladder to this one.
        """
        self += self.previous_ladder

    @property
    def previous_ladder(self):
        """
        Return the ladder for the previous round.
        """
        if self.round.name == 'Round 1':
            return None

        return self.__class__.objects.get(
            round=self.round.previous_round,
            club=self.club
        )

    @property
    def is_bye(self):
        return self.club in self.round.bye_clubs


# Premiership ladders

class BasePremiershipLadder(BaseLadder):
    """
    Base class for AFL and Legends premiership ladders
    """

    # Class attributes
    aggregate_fields = ['position', 'previous_position', 'percentage', 'played']
    has_bonus_strike_rate = False
    has_min_max_for_against = False
    has_strike_rate = False
    is_premiership = True

    sort_order = ('-points', '-percentage', '-score_for', '-win', '-draw')

    played = models.IntegerField(default=0, null=True)
    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    score_for = models.IntegerField(default=0)
    score_against = models.IntegerField(default=0)
    points = models.IntegerField(default=0, null=True)
    percentage = models.FloatField(default=0, null=True)

    class Meta:
        abstract = True

    def update_columns(self, game):
        """
        Update columns in a premiership ladder.
        """
        away = getattr(game, '{}_away'.format(self.prefix))
        away_score = getattr(game, '{}_away_score'.format(self.prefix))
        home_score = getattr(game, '{}_home_score'.format(self.prefix))

        if self.club == away:
            self.score_for += away_score
            self.score_against += home_score
        else:
            self.score_for += home_score
            self.score_against += away_score

        if self.score_for > self.score_against:
            self.win = 1
        elif self.score_for < self.score_against:
            self.loss = 1
        else:
            self.draw = 1

    def calculate_percentage(self):
        """
        Calculate percentage for the AFL and Legends ladders.
        """
        try:
            self.percentage = \
                100 * float(self.score_for) / self.score_against
        except ZeroDivisionError:
            self.percentage = 0

    def calculate_premiership_points(self):
        """
        Calculate premiership points for club.
        """
        self.points = \
            self.win * constants.LadderPoints.WIN_POINTS + \
            self.draw * constants.LadderPoints.DRAW_POINTS

    def calculate_played(self):
        """
        Calculates games played by club.
        """
        self.played = sum(
            getattr(self, attr) for attr in ('win', 'draw', 'loss')
        )

    def finalise(self):
        """
        Add the previous ladder to this one.
        """
        super(BasePremiershipLadder, self).finalise()

        self.calculate_played()
        self.calculate_premiership_points()
        self.calculate_percentage()

        if hasattr(self, 'calculate_min_max_scores'):
            self.calculate_min_max_scores()
        if hasattr(self, 'calculate_average_scores'):
            self.calculate_average_scores()


class AFLLadder(BasePremiershipLadder):

    prefix = 'afl'

    class Meta:
        app_label = 'main'
        db_table = 'main_afl_ladder'


class LegendsLadder(BasePremiershipLadder):

    # Class attributes
    prefix = 'legends'
    has_min_max_for_against = True

    aggregate_fields = [
        'position', 'previous_position', 'percentage', 'played',
        'max_for', 'min_for', 'avg_for',
        'max_against', 'min_against', 'avg_against'
    ]

    bye_for = models.IntegerField(default=0, null=True)
    total_for = models.IntegerField(default=0, null=True)
    max_for = models.IntegerField(default=0, null=True)
    min_for = models.IntegerField(default=0, null=True)
    avg_for = models.FloatField(default=0, null=True)
    max_against = models.IntegerField(default=0, null=True)
    min_against = models.IntegerField(default=0, null=True)
    avg_against = models.FloatField(default=0, null=True)

    class Meta:
        app_label = 'main'
        db_table = 'main_legends_ladder'

    def __unicode__(self):
        return u'%s: %s' % (self.round, self.club)

    def calculate_min_max_scores(self):
        """
        Calculate min/max scores for premiership ladders. Note that the AFL
        ladder doesn't have any.
        """

        previous = self.previous_ladder

        # Min/max scores
        if previous:
            if self.club.has_bye(self.round):
                self.min_for = previous.min_for
                self.max_for = previous.max_for
                self.min_against = previous.min_against
                self.max_against = previous.max_against
            else:
                self.min_for = min(self.score_for, previous.min_for)
                self.max_for = max(self.score_for, previous.max_for)
                if previous.min_against == 0:
                    # We want to override a 0 min_against in the previous round
                    # if club had a bye in Round 1 since that 0 score didn't
                    # actually happen. But we want to record a 0 if someone
                    # actually scores 0...
                    if previous.round.name == 'Round 1' \
                            and self.club.has_bye(previous.round):
                        self.min_against = self.score_against
                else:
                    self.min_against = min(
                        self.score_against, previous.min_against
                    )
                self.max_against = max(self.score_against, previous.max_against)
        else:
            self.min_for = self.score_for
            self.max_for = self.score_for
            self.min_against = self.score_against
            self.max_against = self.score_against

    def calculate_average_scores(self):
        """
        Calculate average scores for Legends ladder.
        """
        if self.played != 0:
            self.avg_for = float(self.score_for) / self.played
            self.avg_against = float(self.score_against) / self.played
        else:
            self.avg_for = 0
            self.avg_against = 0


# Non-premiership ladders

class BaseLegendsLadder(BaseLadder):
    """
    Base class for Brownlow, Coleman, Crowds and Margins ladders.

    """
    # Class attributes
    aggregate_fields = [
        'position', 'previous_position', 'strike_rate', 'bonus_strike_rate',
        'max_score', 'min_score', 'avg_score'
    ]
    has_bonus_strike_rate = False
    has_min_max_for_against = True
    has_strike_rate = True
    is_premiership = False
    completed_statuses = (constants.Round.PROVISIONAL, constants.Round.FINAL)

    # Database columns
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0, null=True)
    min_score = models.IntegerField(default=0, null=True)
    avg_score = models.FloatField(default=0, null=True)
    strike_rate = models.FloatField(default=0, null=True)

    class Meta:

        abstract = True

    def update_columns(self, tip):
        """
        Update columns in a non-premiership ladder
        """
        raise NotImplementedError(
            'ERROR: update_columns() must be implemented in a subclass of {}.'
            .format(self.__class__.__name__)
        )

    def calculate_strike_rates(self):
        """
        Calculate strike rates for a ladder if it has them
        """
        if self.has_strike_rate:
            model = self.__class__.__name__

            num_games = self.completed_games_count

            if model == 'ColemanLadder':
                score_games = self.winners
            else:
                score_games = num_games - self.nothing

            if num_games:
                self.strike_rate = 100.0 * score_games / num_games

                if self.has_bonus_strike_rate:
                    if model == 'MarginsLadder':
                        bonus_games = score_games - self.other
                    elif model == 'ColemanLadder':
                        bonus_games = self.bonus
                    else:
                        bonus_games = self.exact

                    self.bonus_strike_rate = 100.0 * bonus_games / num_games
            else:
                self.strike_rate = 0.00
                if self.has_bonus_strike_rate:
                    self.bonus_strike_rate = 0.00

    def calculate_min_max_scores(self):
        """
        Calculate min/max scores for non-premiership ladders.
        """
        previous = self.previous_ladder

        if previous:
            self.min_score = min(
                self.score - previous.score, previous.min_score
            )
            self.max_score = max(
                self.score - previous.score, previous.max_score
            )
        else:
            self.min_score = self.score
            self.max_score = self.score

    def calculate_average_scores(self):
        """
        Calculate average scores for non-premiership ladders.
        """
        round_count = self.completed_rounds.count()

        # If we're building ladders for this round for the first time, the round
        # will still be scheduled and won't be included in the count
        if self.round.status == constants.Round.SCHEDULED:
            round_count += 1

        self.avg_score = float(self.score) / round_count

    @property
    def completed_rounds(self):
        """
        Find the number of rounds that have been completed. Include provisional
        rounds since we're doing live ladders.
        """
        return Round.objects.filter(
            season=self.round.season, status__in=self.completed_statuses)

    @property
    def completed_games_count(self):
        """
        Find the number of completed AFL games so far this season.
        """
        # Number of games in previous rounds
        completed_rounds = self.completed_rounds.exclude(id=self.round.id)
        count = sum(r.num_games for r in completed_rounds)

        # Games played in this round so far - just get ones with nonzero home
        # and away scores (we'll never get a 0-0:))
        games = self.round.games.filter(
            afl_away_score__gt=0, afl_home_score__gt=0).count()

        return count + games

    def _update_score(self, tip, score_attr):
        """
        Update the given score attribute for a ladder.
        """
        value = getattr(self, 'score') + getattr(tip, score_attr)
        setattr(self, 'score', value)

    def _update_difference_attr(self, value):
        """
        Set a "difference" attribute (e.g. 'exact') on the ladder. Use `value`
        to lookup the attribute to set.
        """
        attr = self.attr_lookup[value]
        value = getattr(self, attr) + 1
        setattr(self, attr, value)

    def finalise(self):
        """
        Add the previous ladder to this one.
        """
        super(BaseLegendsLadder, self).finalise()

        self.calculate_min_max_scores()
        self.calculate_average_scores()
        self.calculate_strike_rates()


class BrownlowLadder(BaseLegendsLadder):

    sort_order = [
        '-score', '-rank_1', '-rank_2', '-rank_3', '-rank_4', '-rank_5']

    # The Brownlow is based on Supercoach rankings
    attr_lookup = {
        10: 'rank_1',
        8: 'rank_2',
        6: 'rank_3',
        4: 'rank_4',
        2: 'rank_5',
        0: 'nothing',
    }

    rank_1 = models.IntegerField(default=0)
    rank_2 = models.IntegerField(default=0)
    rank_3 = models.IntegerField(default=0)
    rank_4 = models.IntegerField(default=0)
    rank_5 = models.IntegerField(default=0)
    nothing = models.IntegerField(default=0)

    class Meta:

        app_label = 'main'
        db_table = 'main_brownlow_ladder'

    def update_columns(self, tip):
        """
        Add the Supercoach scores for tip to a Brownlow ladder.
        """
        self._update_score(tip, 'supercoach_score')

        for sc in tip.supercoach_tips.all():
            self._update_difference_attr(sc.score)


class ColemanLadder(BaseLegendsLadder):

    # Class attributes
    has_bonus_strike_rate = False
    sort_order = ['-score', '-nine', '-eight', '-seven', '-six', '-five',
                  '-four', '-three', '-two', '-one']
    attr_lookup = {
        0: 'nothing',
        1: 'one',
        2: 'two',
        3: 'three',
        4: 'four',
        5: 'five',
        6: 'six',
        7: 'seven',
        8: 'eight',
        9: 'nine'
    }

    # Database columns
    bonus = models.IntegerField(default=0)
    nine = models.IntegerField(default=0)
    eight = models.IntegerField(default=0)
    seven = models.IntegerField(default=0)
    six = models.IntegerField(default=0)
    five = models.IntegerField(default=0)
    four = models.IntegerField(default=0)
    three = models.IntegerField(default=0)
    two = models.IntegerField(default=0)
    one = models.IntegerField(default=0)
    nothing = models.IntegerField(default=0)
    winners = models.IntegerField(default=0)
    bonus_strike_rate = models.FloatField(default=0, null=True)

    class Meta:
        app_label = 'main'
        db_table = 'main_coleman_ladder'

    def update_columns(self, tip):
        """
        Add Coleman score for tip to a Coleman ladder.
        """
        self._update_score(tip, 'winners_score')

    def finalise(self):
        """
        Do some finishing off before we add the previous ladder to this one.
        """
        self.score = self.score / constants.TipPoints.WINNER
        self.winners = self.score

        self._update_difference_attr(self.winners)

        super(ColemanLadder, self).finalise()


class MarginsLadder(BaseLegendsLadder):

    # Class attributes
    has_bonus_strike_rate = True
    sort_order = ['-score', '-exact', '-one', '-two', '-three', '-four',
                  '-five', '-other']
    attr_lookup = {
        20: 'exact',
        18: 'one',
        16: 'two',
        14: 'three',
        12: 'four',
        10: 'five',
    }

    # Database columns
    exact = models.IntegerField(default=0)
    one = models.IntegerField(default=0)
    two = models.IntegerField(default=0)
    three = models.IntegerField(default=0)
    four = models.IntegerField(default=0)
    five = models.IntegerField(default=0)
    other = models.IntegerField(default=0)
    nothing = models.IntegerField(default=0)
    bonus_strike_rate = models.FloatField(default=0, null=True)

    class Meta:

        app_label = 'main'
        db_table = 'main_margins_ladder'

    def update_columns(self, tip):
        """
        Add margin score for tip to a margins ladder.
        """
        self._update_score(tip, 'margins_score')

        if tip.margins_score:
            try:
                self._update_difference_attr(tip.margins_score)
            except KeyError:
                self.other += 1
        else:
            self.nothing += 1


class CrowdsLadder(BaseLegendsLadder):

    # Class attributes
    has_bonus_strike_rate = True
    sort_order = ['-score', '-exact', '-one', '-two', '-three', '-four']
    attr_lookup = {
        8: 'exact',
        4: 'one',
        3: 'two',
        2: 'three',
        1: 'four',
        0: 'nothing'
        }

    # Database columns
    exact = models.IntegerField(default=0)
    one = models.IntegerField(default=0)
    two = models.IntegerField(default=0)
    three = models.IntegerField(default=0)
    four = models.IntegerField(default=0)
    nothing = models.IntegerField(default=0)
    bonus_strike_rate = models.FloatField(default=0, null=True)

    class Meta:

        app_label = 'main'
        db_table = 'main_crowds_ladder'

    def update_columns(self, tip):
        """
        Add crowd score for tip to a crowds ladder.
        """
        self._update_score(tip, 'crowds_score')
        self._update_difference_attr(tip.crowds_score)


class StreakLadder(models.Model):

    sort_order = ['-wins', '-draws', 'losses', 'previous_position']

    club = models.ForeignKey(Club, related_name='streak_ladders')
    losses = models.IntegerField(default=0)
    position = models.IntegerField(default=0, null=True)
    previous_position = models.IntegerField(default=0, null=True)
    round = models.ForeignKey(Round, related_name='streak_ladders')
    streak = models.CharField(max_length=30, default='')
    draws = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)

    class Meta:

        app_label = 'main'
        db_table = 'main_streak_ladder'
        ordering = ['wins', 'draws', '-losses', 'club']

    def add_outcome(self, outcome):
        """
        Update the contents of this ladder with `outcome`.
        """
        # Add outcome to the end of streak
        self.streak += outcome

        # Update wins, draws and losses
        if outcome == 'W':
            self.wins += 1
        elif outcome == 'L':
            self.losses += 1
        elif outcome == 'D':
            self.draws += 1

    def clear(self):
        """
        Clear out the contents of a ladder except for `id`, `club` and `round`.
        """
        excluded = ('id', 'club', 'round')
        for f in [f.name for f in self._meta.fields if f.name not in excluded]:
            if f == 'streak':
                setattr(self, f, '')
            else:
                setattr(self, f, 0)

    def copy_previous(self):
        """
        Copy the contents of the previous Streak ladder into this one.
        Overwrite anything that is already in `self` except `id`, `club` and
        `round`.
        """
        excluded = ('id', 'club', 'round')
        prev = self.previous_ladder
        if prev:
            for f in [f.name for f in self._meta.fields
                      if f.name not in excluded]:
                value = getattr(prev, f, None)
                if f == 'streak':
                    setattr(self, f, '' if value is None else value)
                elif f == 'previous_position':
                    value = prev.position
                    setattr(self, f, '' if value is None else value)
                else:
                    setattr(self, f, 0 if value is None else value)
        else:
            for f in [f.name for f in self._meta.fields
                      if f.name not in excluded]:
                if f == 'streak':
                    setattr(self, f, '')
                else:
                    setattr(self, f, 0)

    def create(self, outcome):
        """
        Create a Streak ladder.
        `outcome` is the outcome of a Legends game (W, D, L or B).
        First, clear the contents of this ladder. Then copy the contents of the
        previous ladder, if there's one, into this one. Finally, add `outcome`.
        """
        self.clear()
        self.copy_previous()
        self.add_outcome(outcome)

    @property
    def previous_ladder(self):
        """
        Return the ladder for the previous round.
        Return None if self.round is Round 1.
        """
        if self.round.name == 'Round 1':
            return None
        else:
            return StreakLadder.objects.get(
                round=self.round.previous_round,
                club=self.club
            )
