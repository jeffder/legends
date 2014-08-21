from django.contrib import admin

import main.models as models


INLINE_MODEL = admin.TabularInline

admin.site.register(models.Season)
admin.site.register(models.Club)
admin.site.register(models.Ground)


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
#    display_extras = ('bye_clubs', )
    list_display = (
        'season', 'name', 'start_time', 'tipping_deadline', 'status')
    list_display_links = ('season', 'name')

#    def __init__(self, *args, **kwargs):
#
#        super(RoundAdmin, self).__init__(*args, **kwargs)
#
#        for extra in self.display_extras:
#            method_name = '_%s' % extra
#            method = getattr(self, method_name)
#
#            setattr(self, extra, method)
#            setattr(getattr(self, extra).im_func, 'short_description', 'Byes')
#            self.list_display += (extra, )
#
#    def _bye_clubs(self, obj):
#        byes = getattr(obj, 'bye_clubs')
#
#        return ', '.join(b.name for b in byes())

admin.site.register(models.Round, RoundAdmin)


class GameAdmin(admin.ModelAdmin):

    fieldsets = [
        (
            None, {
                'fields': (
                    ('round', 'ground'),
                    ('game_date', 'tipping_deadline'),
                    ('status', 'finals_game')
                )
            }
        ),
        ('AFL Teams',
            {'fields': ('afl_home', 'afl_away')}),
        ('Legends Teams',
            {'fields': ('legends_home', 'legends_away')}),
        ('AFL Results',
            {'fields': ('afl_home_score', 'afl_away_score', 'crowd')}),
        ('Legends Results',
            {'fields': ('legends_home_score', 'legends_away_score')}),
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
#    inlines = [AFLBogInline]

admin.site.register(models.Game, GameAdmin)
