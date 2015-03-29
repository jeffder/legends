# Define the forms for the Legends application
#

from django import forms
from django.contrib.auth import authenticate
from django.forms.util import ErrorList

import main.models as models

# Dummy club ID for draw tips
DRAW_TIP = '-99'
EMPTY_VALUE = ''

class Errors(ErrorList):
    '''
        Customise the error list format
    '''

    def __unicode__(self):

        if not self:
            return u''

        return ''.join([e for e in self])


# Authorisation
class LoginForm(forms.Form):
    '''
    Log a user in using a username and password.
    '''

    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'username',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Password'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.user_cache = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(
                username=username,
                password=password
            )
            if self.user_cache is None:
                # No need to be very informative since we're not going to
                # actually use the error message
                raise forms.ValidationError('Error')
        else:
            # No need to be very informative since we're not going to actually
            # use the error message
            raise forms.ValidationError('Error')

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id

        return None

    def get_user(self):
        return self.user_cache


class ChangePasswordForm(forms.Form):
    '''
    Let a user change set his password.
    '''

    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'old-password',
                'placeholder': 'Old password'
            }
        )
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'new-password1',
                'placeholder': 'New password'
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'new-password2',
                'placeholder': 'Confirm new password'
            }
        )
    )

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.user = user

    def clean_old_password(self):
        '''
        Validates that the old_password field is correct.
        '''
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            # No need to be very informative since we're not going to actually
            # use the error message
            raise forms.ValidationError('Error')

        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                # No need to be very informative since we're not going to
                # actually use the error message
                raise forms.ValidationError('Error')
        else:
            # No need to be very informative since we're not going to actually
            # use the error message
            raise forms.ValidationError('Error')

        return password2

    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()

        return self.user


# Tips
class TipForm(forms.ModelForm):
    """
    Submission form for tips
    """

    winner = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={
                'class': 'form-control-inline-select input-sm',
                }
        )
    )
    margin = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-inline input-sm',
                'placeholder': 'Margin'
            }
        )
    )
    crowd = forms.IntegerField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control-inline input-sm',
                'placeholder': 'Crowd'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(TipForm, self).__init__(*args, **kwargs)
        clubs = (self.instance.game.afl_home, self.instance.game.afl_away)
        self.club_lookup = {c.id: c for c in clubs}

        # Set options for fields
        choices = [(c.id, c.name) for c in clubs]

        self.fields['winner'].choices = choices

    class Meta:
        model = models.Tip
        fields = ['winner', 'margin', 'crowd']

    def clean_crowd(self):
        crowd = self.cleaned_data['crowd']

        if crowd < 1000 or crowd > 110000:
            raise forms.ValidationError(
                'Crowd must be between 1,000 and 110,000'
            )

        if crowd % 1000:
            raise forms.ValidationError('Crowd must be a multiple of 1,000')

        return crowd

    def clean_winner(self):
        winner = self.cleaned_data['winner']

        if winner == EMPTY_VALUE:
            raise forms.ValidationError('You have not selected a winner')

        return self.club_lookup.get(int(winner), None)

    def clean(self):
        super(TipForm, self).clean()

        cleaned_data = self.cleaned_data

        winner = cleaned_data.get('winner')
        margin = cleaned_data.get('margin')

        if margin is None:
            return cleaned_data

        if winner:
            if winner.id != DRAW_TIP:
                if margin == 0:
                    del cleaned_data['winner']
                    del cleaned_data['margin']
                    raise forms.ValidationError(
                        'You have not tipped a draw. '
                        'Margin must be at least 1.'
                    )

            if margin != 0 and winner.id == DRAW_TIP:
                del cleaned_data['winner']
                del cleaned_data['margin']
                raise forms.ValidationError(
                    'You have tipped a draw. Margin must be 0'
                )

        return cleaned_data

#    def save(self, *args, **kwargs):
#        cleaned_data = self.cleaned_data
#
#        if not cleaned_data:
#            return self.instance
#
#        winner = self.cleaned_data['winner']
#
#        self.instance.winner = winner
#        self.instance.margin = cleaned_data['margin']
#        self.instance.crowd = cleaned_data['crowd']
#        if cleaned_data['crowd'] == 0 and cleaned_data['margin'] == 1:
#            self.instance.is_default = True
#        else:
#            self.instance.is_default = False
#
#        self.instance.save()
#
#        return self.instance


class SupercoachForm(forms.ModelForm):
    """
    Class for Supercoach forms
    """

    player = forms.ChoiceField(
        widget=forms.Select(
            attrs={'class': 'form-control-inline-select-supercoach input-sm'}
        )
    )

    def __init__(self, players, *args, **kwargs):
        super(SupercoachForm, self).__init__(*args, **kwargs)

        # Set options for fields
        choices = [(EMPTY_VALUE, '--- Select player')]
        choices.extend([(p.id, str(p)) for p in players])

        self.fields['player'].choices = choices

    class Meta:
        model = models.SupercoachTip
        fields = ['player']

    def clean_player(self):
        player = self.cleaned_data['player']

        if player == EMPTY_VALUE:
            raise forms.ValidationError('You have not selected a player')

        return models.Player.objects.get(id=int(player))

#    def save(self, *args, **kwargs):
#        player = self.cleaned_data['player']
#
#        self.instance.player = models.Player.objects.get(id=player)
#
#        self.instance.save()
#
#        return self.instance

#class TipForm(forms.ModelForm):
#    """
#    Submission form for tips
#    """
#
#    winner = forms.ChoiceField(
#        widget=forms.Select(
#            attrs={
#                'class': 'form-control-inline-select',
#                }
#        )
#    )
#    margin = forms.IntegerField(
#        widget=forms.TextInput(
#            attrs={
#                'class': 'form-control-inline',
#                'placeholder': 'Margin'
#            }
#        )
#    )
#    crowd = forms.IntegerField(
#        widget=forms.TextInput(
#            attrs={
#                'class': 'form-control-inline',
#                'placeholder': 'Crowd'
#            }
#        )
#    )
#
#    def __init__(self, *args, **kwargs):
#
#        super(TipForm, self).__init__(*args, **kwargs)
#
#        # Use customised error formatting
#        kwargs['error_class'] = Errors
#
#        print('In form.__init__: instance =', self.instance)
#        self.home = self.instance.game.afl_home
#        self.away = self.instance.game.afl_away
#        self.ground = self.instance.game.ground
#        self.date = self.instance.game.game_date
#
#        clubs = (self.home, self.away)
#
#        self.club_lookup = dict((c.id, c) for c in clubs)
#
#        # Set options for fields
#        choices = [('', 'Winner')]
#        choices.extend([(c.id, c.name) for c in clubs])
#        choices.append((DRAW_TIP, 'Draw'))
#
#        self.fields['winner'].choices = choices
#
#        # Give form fields an id
#        for field in self.fields:
#            self.fields[field].widget.attrs['id'] = 'id-{}-{}'.format(self.instance.id, field)
#
#    class Meta:
#        model = models.Tip
#        fields = ['winner', 'margin', 'crowd']
#
#    def clean_crowd(self):
#
#        print('Cleaning margin')
#        crowd = self.cleaned_data['crowd']
#
#        if crowd < 1000 or crowd > 110000:
#            raise forms.ValidationError(
#                'Crowd must be between 1,000 and 110,000'
#            )
#
#        if crowd % 1000:
#            raise forms.ValidationError('Crowd must be a multiple of 1,000')
#        print('Crowd valid')
#        return crowd
#
#    def clean_winner(self):
#        print('Cleaning winner')
#        winner = self.cleaned_data['winner']
#
#        if not winner:
#            raise forms.ValidationError('Winner must not be blank')
#        print('Winner valid')
#
#        return int(winner)
#
#    def clean(self):
#
#        super(TipForm, self).clean()
#        print('Cleaning winner/margin')
#        cleaned_data = self.cleaned_data
#
#        winner = cleaned_data.get('winner')
#        margin = cleaned_data.get('margin')
#        print('cleaned_data =', cleaned_data)
#        print('winner =', winner)
#        print('margin =', margin)
#        if margin is None:
#            return cleaned_data
#
#        if winner:
#            if winner != DRAW_TIP:
#                if margin == 0:
#                    del cleaned_data['winner']
#                    del cleaned_data['margin']
#                    raise forms.ValidationError(
#                        'You have not tipped a draw. '
#                        'Margin must be at least 1.'
#                    )
#
#            if margin != 0 and winner == DRAW_TIP:
#                del cleaned_data['winner']
#                del cleaned_data['margin']
#                raise forms.ValidationError(
#                    'You have tipped a draw. Margin must be 0'
#                )
#
#        print('Margin valid')
#        return cleaned_data
#
#    def save(self):
#
#        cleaned_data = self.cleaned_data
#
#        if not cleaned_data:
#            return self.instance
#
#        winner = self.cleaned_data['winner']
#        try:
#            winner = self.club_lookup[winner]
#
#        except:
#            winner = None
#
#        self.instance.winner = winner
#        self.instance.margin = cleaned_data['margin']
#        self.instance.crowd = cleaned_data['crowd']
#        if cleaned_data['crowd'] == 0 and cleaned_data['margin'] == 1:
#            self.instance.is_default = True
#        else:
#            self.instance.is_default = False
#
#        self.instance.save()
#
#        return self.instance
#
#
#class SupercoachForm(forms.Form):
#    """
#    Class for Supercoach forms
#    """
#
#    def __init__(self, players, *args, **kwargs):
#        self.instance = kwargs.pop('instance')
#
##        if 'sc_data' in kwargs:
##            self.instance.player = kwargs['sc_data']['player']
#
#        # Use customised error formatting
#        kwargs['error_class'] = Errors
#
#        super(SupercoachForm, self).__init__(*args, **kwargs)
#
#        # Set options for fields
#        choices = [('', 'Supercoach')]
#        choices.extend([(p.id, str(p)) for p in players])
#
#        self.fields['player'].choices = choices
#
#        # Find out if we have a default tip/result
#        if self.instance.tip.is_default:
#            self.fields['player'].initial = ''
#        else:
#            self.fields['player'].initial = self.instance.player.id
#
#    player = forms.ChoiceField(
#        widget=forms.Select(
#            attrs={'class': 'form-control-inline-select-supercoach'}
#        )
#    )
#
#    def clean_player(self):
#        player = self.cleaned_data['player']
#
#        if not player:
#            raise forms.ValidationError('Player must not be blank')
#
#        return int(player)
#
#    def save(self):
#        player = self.cleaned_data['player']
#
#        self.instance.player = models.Player.objects.get(id=int(player))
#
#        self.instance.save()
#
#        return self.instance


class LadderForRoundForm(forms.Form):
    '''
    Selection of round and ladder name in past years (post 2008) view.
    '''

    def __init__(self, *args, **kwargs):

        for attr in ('rnd', 'ladder_name', 'rounds'):
            try:
                setattr(self, attr, kwargs.pop(attr))
            except KeyError:
                setattr(self, attr, args[0].get(attr))

        super(LadderForRoundForm, self).__init__(*args, **kwargs)

        if not self.rounds:
            season = models.Round.objects.get(id=int(self.rnd)).season
            self.rounds = season.rounds   \
                .filter(is_finals=False, status__in=('Provisional', 'Final'))

        round_choices = [(r.id, r.name) for r in self.rounds]
        ladder_choices = [
            ('legends', 'Legends'),
            ('coleman', 'Coleman'),
            ('brownlow', 'Brownlow'),
            ('margins', 'Margins'),
            ('crowds', 'Crowds'),
            ('streak', 'Form Guide'),
            ('afl', 'AFL'),
        ]

        self.fields['rnd'].choices = round_choices
        self.fields['rnd'].initial = self.rnd or self.rounds[0].id
        self.fields['rnd'].required = True

        self.fields['ladder_name'].choices = ladder_choices
        self.fields['ladder_name'].initial = self.ladder_name or 'legends'
        self.fields['ladder_name'].required = True

    rnd = forms.ChoiceField()
    ladder_name = forms.ChoiceField()


class LadderForRoundFormPre2008(forms.Form):
    '''
    Selection of round and ladder name in past years (pre 2008) view.
    '''

    def __init__(self, *args, **kwargs):

        for attr in ('ladder_name', 'season'):
            try:
                setattr(self, attr, kwargs.pop(attr))
            except KeyError:
                setattr(self, attr, args[0].get(attr))

        super(LadderForRoundFormPre2008, self).__init__(*args, **kwargs)

        ladder_choices = [
            ('legends', 'Legends'),
            ('coleman', 'Coleman'),
            ('brownlow', 'Brownlow'),
        ]

        if self.season.season == 2007:
            ladder_choices.extend([
                ('crowds', 'Crowds'),
                ('margins', 'Margins'),
            ])

        self.fields['ladder_name'].choices = ladder_choices
        self.fields['ladder_name'].initial = self.ladder_name or 'legends'
        self.fields['ladder_name'].required = True

    ladder_name = forms.ChoiceField()


class CoachVCoachForm(forms.Form):
    '''
    Selection of coaches for the coach versus coach view.
    '''

    def __init__(self, *args, **kwargs):

        for attr in ('coach_1', 'coach_2', 'coaches'):
            try:
                setattr(self, attr, kwargs.pop(attr))
            except KeyError:
                setattr(self, attr, args[0].get(attr))

        super(CoachVCoachForm, self).__init__(*args, **kwargs)

        # Get the coach names
        if not self.coaches:
            def _sort_key(name):
                first, last = name.split(' ', 1)
                return (last.lower(), first.lower())

            self.coaches = sorted(
                {c.name for c in models.Coach.objects.all()},
                key=_sort_key
            )

        assistants = ('Bernard Bialecki', 'Ben West', 'Peter Moran',
                      'Chris Balkos')
        choices = [(c, c) for c in self.coaches if c not in assistants]

        self.fields['coach_1'].choices = choices
        self.fields['coach_1'].initial = self.coach_1 or self.coaches[0]
        self.fields['coach_1'].required = True

        self.fields['coach_2'].choices = choices
        self.fields['coach_2'].initial = self.coach_2 or self.coaches[0]
        self.fields['coach_2'].required = True

    coach_1 = forms.ChoiceField()
    coach_2 = forms.ChoiceField()


class ClubSelectionForm(forms.Form):
    '''
    Selection of club for the manual tips view.
    '''

    def __init__(self, *args, **kwargs):

        for attr in ('curr_round', 'club', 'clubs'):
            try:
                setattr(self, attr, kwargs.pop(attr))
            except KeyError:
                setattr(self, attr, args[0].get(attr))

        super(ClubSelectionForm, self).__init__(*args, **kwargs)

        # Get the club names
        if not self.clubs:
            self.clubs = [c for c in self.curr_round.season.clubs()
                          if c.can_tip_in_round(self.curr_round)]

        choices = [(c.id, c) for c in self.clubs]
        self.fields['club'].choices = choices
        self.fields['club'].initial = self.club.id or self.clubs[0].id
        self.fields['club'].required = True

    club = forms.ChoiceField()
