from django.contrib.auth.models import User
from django.db import models
from django.db.models.loading import get_model

from main import constants


class Club(models.Model):

    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    user = models.ForeignKey(User, unique=True, related_name='clubs')

    class Meta:
        app_label = 'main'
        ordering = ['name']

    def __str__(self):
        return self.name

    def players_by_season(self, season):
        """
        Return all the club's players for the given season.
        """
        return self.players.filter(season=season).all()

    def has_bye(self, rnd):
        """
        See if club has a bye in the given round.
        """
        return self in rnd.bye_clubs

    def create_default_tip(self, game):
        """
        Create a default tip for this club for game.
        """
        model = get_model('main', 'Tip')
        tip = model(
            club=self,
            game=game,
            is_default=True
        )
        tip.save()

        # Supercoach tips
        model = get_model('main', 'SupercoachTip')

        rnd = game.round
        if not rnd.is_finals:
            sc_count = constants.Supercoach.SC_COUNT_HOME_AWAY
        elif rnd.name != 'Grand Final':
            sc_count = constants.Supercoach.SC_COUNT_GRAND_FINAL
        else:
            sc_count = constants.Supercoach.SC_COUNT_FINALS

        for _ in range(sc_count):
            sc_tip = model(tip=tip)
            sc_tip.save()
