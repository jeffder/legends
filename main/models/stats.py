from collections import OrderedDict
#import cookielib
import datetime
from itertools import groupby
#import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from main.models import Club, Game, Round, Season


# Models for the various stats pages

class PastCategoryWinner(models.Model):
    '''
    Model for past category winners which allows for ties.
    '''

    category = models.CharField(max_length=20)
    club = models.ForeignKey(
        Club, related_name='past_category_winners', null=True
    )
    season = models.ForeignKey(Season, related_name='past_category_winners')

    class Meta:

        app_label = 'main'
        db_table = 'main_past_category_winner'
        ordering = ('-season', 'category', 'club')
        verbose_name_plural = 'Past Winners'


class PastCoach(models.Model):
    '''
    A stripped down version of the Coach model for pre-2008 stats.
    '''

    club = models.ForeignKey(Club, related_name='past_coaches')
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, null=True)
    season = models.ForeignKey(Season, related_name='past_coaches')

    class Meta:

        app_label = 'main'
        db_table = 'main_past_coach'
        verbose_name_plural = 'past_coaches'
        ordering = [
            '-season', 'club', 'last_name', 'first_name'
        ]

    def __unicode__(self):

        return '%s - %s - %s' % (self.season, self.club.name, self.name())

    @property
    def name(self):
        '''
            Return the coach's full name as first_name last_name.
        '''

        return ' '.join((self.first_name, self.last_name))


class BasePastLadder(models.Model):
    '''
        A base class for pre-2008 ladders
    '''
    sort_order = ['position', '-score', 'club']

    club = models.ForeignKey(Club, related_name='%(class)ss')
    avg_score = models.FloatField(default=0)
    position = models.IntegerField(default=0, null=True)
    score = models.IntegerField(default=0)
    season = models.ForeignKey(Season, related_name='past_%(class)ss')

    class Meta:

        abstract = True


class PastLegendsLadder(BasePastLadder):
    '''
        A stripped down model for pre-2008 Legends ladders
    '''

    sort_order = (
        'position', '-score', 'percentage', '-points_for', '-win', '-draw',
        'club'
    )

    played = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    draw = models.IntegerField(default=0)
    loss = models.IntegerField(default=0)
    points_for = models.IntegerField(default=0)
    points_against = models.IntegerField(default=0)
    avg_points_for = models.FloatField(default=0)
    avg_points_against = models.FloatField(default=0)
    percentage = models.FloatField(default=0)

    class Meta:

        app_label = 'main'
        db_table = 'main_past_legends_ladder'


class PastBrownlowLadder(BasePastLadder):

    class Meta:

        app_label = 'main'
        db_table = 'main_past_brownlow_ladder'


class PastColemanLadder(BasePastLadder):

    class Meta:

        app_label = 'main'
        db_table = 'main_past_coleman_ladder'


class PastCrowdsLadder(BasePastLadder):

    class Meta:

        app_label = 'main'
        db_table = 'main_past_crowds_ladder'


class PastMarginsLadder(BasePastLadder):

    class Meta:

        app_label = 'main'
        db_table = 'main_past_margins_ladder'


