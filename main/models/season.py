from django.db import models
from django.db.models import Q

from main import constants


class Season(models.Model):

    season = models.IntegerField(null=False)

    # Every season from 2008 has full data (coaches, games, tips, results,
    # ladders etc). The rest have some ladders and category winners except
    # 2006...
    has_full_data = models.BooleanField(default=True)

    # ...which has no data except the Premier.
    has_no_data = models.BooleanField(default=False)

    class Meta:
        app_label = 'main'
        ordering = ['-season']

    def __str__(self):
        return '{}'.format(self.season)

    @property
    def live_round(self):
        """
        Return the round currently being played for this season.
        It will be the earliest non-final round in the season or the Grand Final
        Round if all rounds are final.
        """
        rounds = self.rounds   \
            .exclude(status=constants.Round.FINAL)   \
            .exclude(start_time=None)

        if rounds:
            return rounds[0]

        # All rounds have status of 'Final' so return the Grand Final round for
        # season
        return self.rounds.get(name='Grand Final')

    @property
    def games_played(self):
        """
        Return the number of games that have been played so far this season.
        """
        return self.games.exclude(status=constants.Game.SCHEDULED).count()

    def club_games_played(self, club):
        """
        Return the number of games that have been played by the club so far this
        season.
        """
        return self.games   \
            .filter(Q(afl_away=self.club) | Q(afl_home=self.club))   \
            .exclude(status=constants.Game.SCHEDULED)   \
            .count()

    @property
    def clubs(self):
        """
        Return the clubs playing this season.
        """
        return set(c.club for c in self.coaches.all())
