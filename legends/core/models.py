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

    def __str__(self):
        return self.season

    class Meta:
        ordering = ['-season']


class Club(models.Model):

    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10)
    user = models.ForeignKey(User, unique=True, related_name='clubs')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Coach(models.Model):

    club = models.ForeignKey(Club, related_name='coaches')
    first_name = models.CharField(max_length=30, null=True)
    has_paid_fees = models.BooleanField(default=False)
    last_name = models.CharField(max_length=30, null=True)
    season = models.ForeignKey(Season, related_name='coaches')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'coaches'
        ordering = ['-season', 'club', 'last_name', 'first_name']

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
    supercoach_name = models.CharField(max_length=30)

    def __str__(self):
        return '{} ({})'.format(self.name, self.club.nickname)

    class Meta:
        ordering = ['-season', 'club', 'last_name', 'initial', 'first_name']

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


class Captain(models.Model):

    # A club can have more than one captain in real life but we restrict each
    # club to one captain for this competition.
    club = models.ForeignKey('Club', related_name='club_captain')
    player = models.ForeignKey('Player', related_name='player_captain')

    def __str__(self):
        return self.player.name

    class Meta:
        ordering = ('-player__season', 'club')


#class Round(models.Model):
#    pass
#
#
class Venue(models.Model):

    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.name
