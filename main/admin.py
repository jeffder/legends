from django.contrib import admin

import main.models as models


INLINE_MODEL = admin.TabularInline

admin.site.register(models.Season)
admin.site.register(models.Club)
admin.site.register(models.Ground)
admin.site.register(models.LegendsLadder)


class CoachAdmin(admin.ModelAdmin):

    list_filter = ('season', 'club')
    list_display = (
        'season', 'club', 'first_name', 'last_name',
        'has_paid_fees', 'is_assistant'
    )
    list_display_links = ('club', )

admin.site.register(models.Coach, CoachAdmin)


class PlayerAdmin(admin.ModelAdmin):

    list_display = ('season', 'club', 'player_name', 'supercoach_name')
    list_display_links = list_display
    list_filter = ('season', 'club')
    ordering = ('season', 'club', 'last_name', 'initial', 'first_name')

    def player_name(self, obj):
        '''
            Return the player's full name as first_name initial last_name.
        '''
        if obj.initial:
            return '{} {}. {}'.format(
                obj.first_name, obj.initial, obj.last_name)
        else:
            return '{} {}'.format(obj.first_name, obj.last_name)

admin.site.register(models.Player, PlayerAdmin)


class RoundAdmin(admin.ModelAdmin):

    list_filter = ('season', )
    list_display = (
        'season', 'name', 'start_time', 'tipping_deadline',
        'bye_clubs', 'status'
    )
    list_display_links = ('season', 'name')

    def bye_clubs(self, obj):
        byes = obj.byes.all()

        return ', '.join(b.club.name for b in byes)

admin.site.register(models.Round, RoundAdmin)


class SupercoachRankingInline(admin.TabularInline):

    extra = 0
    model = models.SupercoachRanking


class GameAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None, {
                'fields': (
                    ('round', 'ground'),
                    ('game_date', 'tipping_deadline'),
                    ('status', 'finals_game', 'is_manual_result')
                )
            }
        ),
        ('AFL Teams',
            {'fields': (('afl_home', 'afl_away'), )}),
        ('AFL Results',
            {'fields': (('afl_home_score', 'afl_away_score', 'crowd'), )}),
        ('Legends Teams',
         {'fields': (('legends_home', 'legends_away'), )}),
        ('Legends Results - Home',
            {
                'fields': (
                    'legends_home_score',
                    (
                        'legends_home_winners_score',
                        'legends_home_winners_bonus'
                    ),
                    'legends_home_margins_score',
                    'legends_home_crowds_score',
                    'legends_home_supercoach_score',
                )
            }
         ),
        ('Legends Results - Away',
            {
                'fields': (
                    'legends_away_score',
                    (
                        'legends_away_winners_score',
                        'legends_away_winners_bonus'
                    ),
                    'legends_away_margins_score',
                    'legends_away_crowds_score',
                    'legends_away_supercoach_score',
                )
            }
         ),
    ]
    list_filter = ('round__season', 'round')
    list_display = (
        'round',
        'afl_home', 'afl_away',
        'ground', 'game_date',
        'tipping_deadline', 'status',
        'legends_home', 'legends_away',
    )
    list_display_links = list_display
    inlines = [SupercoachRankingInline]

admin.site.register(models.Game, GameAdmin)


class SupercoachRankingAdmin(admin.ModelAdmin):

    list_filter = ('game__round__season', 'player__club')

admin.site.register(models.SupercoachRanking, SupercoachRankingAdmin)


class SupercoachTipInline(INLINE_MODEL):

    model = models.SupercoachTip

    extra = 0
    ordering = ['player__last_name', 'player__initial', 'player__first_name']


class TipAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None, {
                'fields': (('game', 'club', 'is_default'), )
            }
        ),
        ('Tips',
            {'fields': (('winner', 'margin', 'crowd'), )}),
        ('Tip Scores',
            {'fields': (
                ('winners_score', 'margins_score', 'crowds_score',
                 'supercoach_score', 'score'),
            )}),
    ]

    inlines = [SupercoachTipInline]
    list_display = (
        'season', 'club', 'round', 'game', 'winner', 'margin', 'crowd',
        'is_default')
    list_display_links = list_display
    list_filter = ('game__round__season', 'club', 'game__round')
    ordering = ('club', )
    search_fields = (
        'club__name',
        '=club__nickname',
        'game__round__name',
        '=game__round__season__season',
        '^game__afl_home__name',
        '^game__afl_away__name'
    )

    def season(self, obj):
        return obj.game.round.season.season
    season.short_description = 'Season'

    def round(self, obj):
        return obj.game.round.name
    round.short_description = 'Round'

admin.site.register(models.Tip, TipAdmin)
