from django.db import models

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
        return self.rounds.filter(name='Grand Final')[0]
