# Statistics views

from collections import OrderedDict
from itertools import groupby

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.db.models.loading import get_model
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext

from main import constants
from main.forms import (
    CoachVCoachForm, LadderForRoundForm, LadderForRoundFormPre2008
)
from main.models import (
    Club, Coach, Game, Bye, Round, Season, Tip,
    PastCoach, PastCategoryWinner,
    LegendsLadder, ColemanLadder, BrownlowLadder,
    CrowdsLadder, MarginsLadder,
    StreakLadder, PastLegendsLadder, PastColemanLadder, PastBrownlowLadder,
    PastCrowdsLadder, PastMarginsLadder
)
from main.views import ladders, tips_and_results
#from main.utils import avg

selected_page = 'stats'
selected_stats = 'rules'

SEASONS = Season.objects.all()
CLUBS = Club.objects.all()

@login_required
def view_stats(request, **kwargs):
    '''
    View various kinds of statistics.
    '''

    if request.method == 'POST':
        form_lookup = {
            'past_years': process_ladder_for_round_form,
            'coach_v_coach': process_coach_v_coach_form,
        }

        return form_lookup[kwargs['view_name']](request, **kwargs)
    else:
        view_lookup = {
            'rules': render_rules,
            'coaches': render_coaches,
            'past_winners': render_past_winners,
            'past_years': render_past_years,
            'coach_v_coach': render_coach_v_coach,
            #'records': render_records,
        }

        view_name = kwargs.pop('view_name', 'rules')
        if view_name in ('past_years', 'coach_v_coach'):
            view = view_lookup[view_name](request, **kwargs)
        else:
            view = view_lookup[view_name](request)

        stats_nav = render_stats_nav(request, view_name)

        auth_form = tips_and_results.render_auth_form(request)

        content = stats_nav + view + auth_form

        return render_to_response(
            'main.html',
            {'content': content,
             'live_round': Round.objects.get(id=request.session['live_round']),
             'club': Club.objects.get(id=request.session['club']),
             'selected_page': selected_page, },
            context_instance=RequestContext(request)
        )


def render_stats_nav(request, active_stats):
    """
    Render the stats nav.
    """
    stats_names = OrderedDict()
    stats_names['rules'] = 'Rules'
    stats_names['coaches'] = 'Coaches'
    stats_names['past_winners'] = 'Past Winners'
    stats_names['past_years'] = 'Past Years'
    stats_names['coach_v_coach'] = 'Coach v Coach'
    #stats_names['Records'] = 'records'

    stats_nav = render(
        request,
        'stats_nav.html',
        {
            'active_stats': active_stats,
            'stats_names': stats_names
        },
    )

    return stats_nav.content


def render_rules(request):
    '''
        Display the competition rules.
    '''

    rendered = render(
        request,
        'view_rules.html',
    )

    return rendered.content


def render_coaches(request):
    '''
        Display the Legends coaches.
    '''

    coaches = Coach.objects.all().order_by('club', '-season')
    past_coaches = PastCoach.objects.all().order_by('club', '-season')

    data = {}

    for qs in (coaches, past_coaches):
        for coach in qs:
            if coach.season not in data:
                data[coach.season] = OrderedDict()
            if coach.club not in data[coach.season]:
                data[coach.season][coach.club] = []

            data[coach.season][coach.club].append(coach.name)

    seasons = sorted(data.keys(), key=sort_key_season)
    clubs = sorted(data[seasons[0]].keys(), key=sort_key_club)
    seasons = reversed(seasons)
    rendered = render(
        request,
        'view_coaches.html',
        {'data': data,
         'clubs': clubs,
         'seasons': seasons}
    )

    return rendered.content


def render_coaches_by_club(request):
    '''
        Display the Legends coaches.

        NOTE: Not currently used.
    '''

    coaches = Coach.objects.all().order_by('club', '-season')
    past_coaches = PastCoach.objects.all().order_by('club', '-season')

    data = {}

    for qs in (coaches, past_coaches):
        for coach in qs:
            if coach.club not in data:
                data[coach.club] = OrderedDict()
            if coach.season not in data[coach.club]:
                data[coach.club][coach.season] = []

            data[coach.club][coach.season].append(coach.name())

    clubs = sorted(data.keys(), key=sort_key_club)
    seasons = reversed(sorted(data[clubs[0]].keys(), key=sort_key_season))
    rendered = render(
        request,
        'view_coaches.html',
        {'data': data,
         'clubs': clubs,
         'seasons': seasons}
    )

    return rendered.content


def render_past_winners(request):
    '''
        Display past winners. We need to allow for joint coaches.
    '''

    past = PastCategoryWinner.objects.all()
    seasons = Season.objects.all().order_by('-season')
    live_season = Season.objects.get(season=request.session['live_season'])

    data = OrderedDict()
    for season in seasons:
        if season == live_season:
            continue

        data[season] = {}
        for category in constants.PrizeCategories.categories:
            data[season][category] = []
            winners = past.filter(season=season, category=category)
            for winner in winners:
                club = winner.club
                if club is not None:
                    if season.season < 2008:
                        qs = club.past_coaches.all()
                    else:
                        qs = club.coaches.all()
                    coaches = [c.name for c in qs.filter(season=season)]
                    data[season][category].append(
                        {'club': club, 'coaches': coaches})
                else:
                    data[season][category].append(
                        {'club': '', 'coaches': ['']})

    rendered = render(
        request,
        'view_past_winners.html',
        {'data': data},
    )

    return rendered.content


def render_past_years(request, season_id=None, round_id=None, ladder=None):
    '''
        Display past years results and ladders.
    '''

    # Get the selected season
    seasons = Season.objects.all()
    if season_id:
        selected_season = Season.objects.get(season=season_id)
    else:
        selected_season = seasons[0]

    # We don't have a lot of the info for seasons before 2008 so we need to
    # handle them differently
    post_2008 = selected_season.season >= 2008

    # Render the Legends ladder by default
    selected_ladder = ladder or 'legends'

    # Get the selected round
    # This will be the last home/away round by default. It may also be the last
    # round from the previous season if we're at the start of a season where no
    # games have been played.
    if post_2008:
        season, rounds, ladder_rounds = get_rounds(selected_season)
        if selected_season != season:
            seasons = seasons[1:]
            selected_season = season
            round_id = None

        if round_id:
            selected_round = ladder_rounds.get(id=round_id)
        else:
            selected_round = ladder_rounds.reverse()[0]

        selector_args = (request, selected_season, selected_ladder)
        selector_kwargs = {
            'rnd': selected_round,
            'rounds': ladder_rounds,
            'post_2008': post_2008
        }
        ladder_args = (request, selected_ladder)
        ladder_kwargs = {
            'round': selected_round,
            'post_2008': post_2008
        }
    else:
        selector_args = (request, selected_season, selected_ladder)
        selector_kwargs = {'post_2008': post_2008}
        ladder_args = (request, selected_ladder)
        ladder_kwargs = {
            'season': selected_season,
            'post_2008': post_2008
        }

    # Render the view
    content = render_season_nav(request, selected_season, seasons)
    content += render_ladder_selector(*selector_args, **selector_kwargs)
    content += render_ladder(*ladder_args, **ladder_kwargs)
    if post_2008:
        content += render_legends_fixtures(request, selected_season, rounds)

    return content


def render_coach_v_coach(request, coach_1=None, coach_2=None):
    '''
        Display head to head results for coach_1 and coach_2.
    '''

    # Get the coach names
    def _sort_key(name):
        first, last = name.split(' ', 1)
        return (last.lower(), first.lower())

    coaches = sorted({c.name for c in Coach.objects.all()}, key=_sort_key)

    # Render the view
    content = render_coach_v_coach_selector(request, coach_1, coach_2, coaches)
    content += render_coach_v_coach_results(request, coach_1, coach_2)

    return content


def render_records(request):
    '''
        Display various records e.g most wins in season
    '''
    records = get_all_records()

    # Temporary until do template
    return 'foo'


def render_season_nav(request, season, seasons):
    '''
    Render season navigation.

    Args:
        * 'season': the currently selected Season (latest season by default)
        * 'seasons': a queryset containing all of the existing seasons
    '''

    season_nav = render(
        request,
        'season_nav.html',
        {'seasons': seasons,
         'selected_season': season},
    )

    return season_nav.content


def render_ladder_selector(
        request, season, ladder_name, rnd=None, rounds=None, post_2008=True):
    '''
    Render the round and ladder form.
    '''

    if post_2008:
        form = LadderForRoundForm(
            rnd=rnd.id,
            ladder_name=ladder_name,
            rounds=rounds
        )
        url = '/legends/stats/past_years/{}/{}/{}/'.format(
            season,
            rnd.id,
            ladder_name
        )
        template = 'ladder_round_form.html'
    else:
        form = LadderForRoundFormPre2008(
            ladder_name=ladder_name, season=season)
        ladder_name = 'past_{}'.format(ladder_name)
        url = '/legends/stats/past_years/{}/{}/'.format(season, ladder_name)
        template = 'ladder_round_form_pre_2008.html'

    rendered = render(
        request,
        template,
        {'form': form,
         'url': url}
    )

    return rendered.content


def render_coach_v_coach_selector(request, coach_1, coach_2, coaches):
    '''
    Render the coach versus coach form.
    '''

    form = CoachVCoachForm(coach_1=coach_1, coach_2=coach_2, coaches=coaches)
    url = '/legends/stats/coach_v_coach/{}/{}/'.format(coach_1, coach_2)

    rendered = render(
        request,
        'coach_v_coach_form.html',
        {'form': form, 'url': url}
    )

    return rendered.content


def render_ladder(request, ladder_name, round=None, season=None, post_2008=True):
    '''
    Render a ladder given the season, round and ladder name.
    '''

    if post_2008:
        rendered = ladders.render_ladder(
            request,
            ladder_name=ladder_name,
            selected_round=round,
        )
    else:
        rendered = render_past_ladder(
            request,
            ladder_name=ladder_name,
            season=season
        )

    return rendered


def render_past_ladder(request, ladder_name, season):
    '''
    Render a past ladder given the season and ladder name.
    '''

    model = globals()['Past%sLadder' % ladder_name.title()]
    model = get_model('main', 'Past{}Ladder'.format(ladder_name.title()))

    template = 'view_past_{}_ladder.html'.format(ladder_name)

    ladder = model.objects.filter(season=season).order_by('position')

    content = render_to_response(
        template,
        {
            'season': season,
            'ladder': ladder
        },
        context_instance=RequestContext(request)
    )

    return content.content


def render_legends_fixtures(request, season, rounds):
    '''
    Render the legends fixtures/results for the selected season.
    '''

    results = Game.objects \
        .filter(round__in=rounds) \
        .order_by('round', 'legends_home')
    byes = Bye.objects \
        .filter(round__in=rounds) \
        .order_by('round', 'club')
    club = Club.objects.get(id=request.session['club'])

    fixture_data = {rnd.name: list(group)
                    for rnd, group in groupby(results, key=results_group_key)}
    bye_data = {rnd.name: list(group)
                for rnd, group in groupby(byes, key=results_group_key)}

    results = render(
        request,
        'season_fixtures.html',
        {'club': club,
         'fixture_data': fixture_data,
         'bye_data': bye_data,
         'rounds': rounds},
    )

    return results.content


def score_detail_header(request, fixture_id):
    '''
    Return the header for a club's scoring details in a specified round.
    '''

    fixture = Game.objects.get(id=fixture_id)

    return render_to_response(
        'score_detail_header.html',
        {'round': fixture.round,
         'fixture': fixture},
        context_instance=RequestContext(request)
    )


def bye_score_detail_header(request, bye_id):
    '''
    Return the header for a bye club's scoring details in a specified round.
    '''

    bye = Bye.objects.get(id=bye_id)
    rnd = Round.objects.get(id=bye.round.id)
    club = Club.objects.get(id=bye.club.id)

    return render_to_response(
        'bye_score_detail_header.html',
        {'round': rnd,
         'score': bye.score,
         'club': club},
        context_instance=RequestContext(request)
    )


def score_detail(request, fixture_id):
    '''
    Return scoring details for a club in a specified round.
    '''

    fixture = Game.objects.get(id=fixture_id)
    rnd = Round.objects.get(id=fixture.round.id)
    home = Club.objects.get(id=fixture.legends_home.id)
    home_tips = home.tips_for_round(rnd)

    away = Club.objects.get(id=fixture.legends_away.id)
    away_tips = away.tips_for_round(rnd)

    tips = [(h, a) for h, a in zip(home_tips, away_tips)]

    return render_to_response(
        'score_detail.html',
        {'round': rnd,
         'fixture': fixture,
         'tips': tips},
        context_instance=RequestContext(request)
    )


def bye_score_detail(request, bye_id):
    '''
    Return bye scoring details for a club in a specified round.
    '''

    bye = Bye.objects.get(id=bye_id)
    rnd = Round.objects.get(id=bye.round.id)
    club = Club.objects.get(id=bye.club.id)

    tips = club.tips_for_round(rnd)

    return render_to_response(
        'bye_score_detail.html',
        {'round': rnd,
         'club': club,
         'tips': tips},
        context_instance=RequestContext(request)
    )


def render_coach_v_coach_results(request, coach_1, coach_2):
    '''
    Render a list of coach head to head results given two coaches names.
    '''

    if coach_1 is None or coach_2 is None:
        return b''

    first_1, last_1 = coach_1.split(' ', 1)
    first_2, last_2 = coach_2.split(' ', 1)

    coaches_1 = Coach.objects.filter(first_name=first_1, last_name=last_1)
    coaches_2 = Coach.objects.filter(first_name=first_2, last_name=last_2)

    legends_results = [
        {
            'result': r,
            'h_coach': c1.name if c1.club == r.legends_home else c2.name,
            'a_coach': c1.name if c1.club == r.legends_away else c2.name
        }
        for c1 in coaches_1
        for c2 in coaches_2
        for r in Game.objects
            .filter(round__status__in=('Provisional', 'Final'))
            .filter(round__season=c1.season)
            .filter(round__season=c2.season)
            .filter(
                Q(legends_home=c1.club) & Q(legends_away=c2.club) |
                Q(legends_home=c2.club) & Q(legends_away=c1.club)
            ).order_by('round')
    ]

    # Summarise coach wins
    summary = {
        'coach_1': coach_1,
        'coach_2': coach_2,
        'coach_1_wins': 0,
        'coach_2_wins': 0,
        'draws': 0,
    }
    for result in legends_results:
        winner = result['result'].legends_winner

        if winner is None:
            summary['draws'] += 1
            continue

        try:
            coaches_1.get(
                club=winner, season=result['result'].round.season)
            summary['coach_1_wins'] += 1
        except Coach.DoesNotExist:
            summary['coach_2_wins'] += 1

    context = {'results': reversed(legends_results)}
    if legends_results:
        context['summary'] = summary

    results = render(
        request,
        'view_coach_v_coach.html',
        context
    )

    return results.content


### Form processing

def process_ladder_for_round_form(request, **kwargs):
    '''
    Process the form for the past years view.
    '''

    season_id = int(kwargs['season_id'])
    season = Season.objects.get(season=season_id)

    post_2008 = season_id >= 2008
    if post_2008:
        form = LadderForRoundForm(request.POST)

        if form.is_valid():
            rnd = form.cleaned_data['rnd']
            rnd = Round.objects.get(id=int(rnd))
            ladder = form.cleaned_data['ladder_name']

            url = '/legends/stats/past_years/{}/{}/{}/'.format(
                rnd.season.season,
                rnd.id,
                ladder
            )
            return redirect(url)
    else:
        ladder = kwargs['ladder'] or 'legends'
        form = LadderForRoundFormPre2008(
            request.POST, season=season, ladder_name=ladder)

        if form.is_valid():
            ladder = form.cleaned_data['ladder_name']

            url = '/legends/stats/past_years/{}/{}/'.format(season, ladder)
            return redirect(url)


def process_coach_v_coach_form(request, **kwargs):
    '''
    Process the form for the coach versus coach view.
    '''

    form = CoachVCoachForm(request.POST)
    if form.is_valid():
        coach_1 = form.cleaned_data['coach_1']
        coach_2 = form.cleaned_data['coach_2']

        url = '/legends/stats/coach_v_coach/{}/{}/'.format(
            coach_1,
            coach_2,
        )

        return redirect(url)


### Helper functions

def get_rounds(season):
    '''
    Return the rounds with ladders for the season.
    '''
    rounds = Round.objects.filter(season=season)
    ladder_rounds = rounds.filter(
        is_finals=False,
        status__in=('Provisional', 'Final')
    )

    # Make sure we got something since we might be at the start of a season
    # where no games have been played
    if not ladder_rounds:
        prev_season = Season.objects.get(season=season.season - 1)
        season, rounds, ladder_rounds = get_rounds(prev_season)

    # TODO: Should be prev_season below???
    return season, rounds, ladder_rounds


def sort_key_club(club):
    return club.name


def sort_key_season(season):
    return season.season


def results_group_key(result):
    return result.round


def get_all_records():
    '''
    Return the records for each given season.
    '''
    season_records = {}
    round_records = {}

    round_scores = Tip.objects   \
        .exclude(afl_fixture__round__status='Scheduled')   \
        .exclude(afl_fixture__round__is_finals=True)   \
        .filter(afl_fixture__round__season=2014)   \
        .values('afl_fixture__round__season', 'afl_fixture__round', 'club')   \
        .annotate(
            round_total=Sum('total'),
            round_winners=Sum('winner_score'),
            round_margins=Sum('margin_score'),
            round_crowds=Sum('crowd_score'),
            round_bogs=Sum('bog_score')
        )   \
        .order_by('afl_fixture__round__season', 'club', 'afl_fixture__round')

    # Get round records
    def _season_key(row):
        return (row['afl_fixture__round__season'], row['club'])

#    def _max(group, key):
#        '''
#        Return the maximum score and the round it was scored in the group
#        '''
#        sorted_group = sorted(group, key=)
#
#        return (row['afl_fixture__round__season'], row['club'])
#
#    def _season_min_key(row):
#        return (row['afl_fixture__round__season'], row['club'])

    for attr in ('total', 'winners', 'margins', 'crowds', 'bogs'):
        attr_key = 'round_%s' % attr
        scores = round_scores.order_by(
            'afl_fixture__round__season',
            'club',
            attr_key,
            'afl_fixture__round'
        )
        for key, group in groupby(scores, key=_season_key):
            club_records = {}

            group = list(group)
            season = key[0]
            club = Club.objects.get(id=key[1])
            if club in club_records:
                club_records[club].update(
                    {
                        'total_%s' % attr: sum(g[attr_key] for g in group),
                        'max_%s' % attr: max(g[attr_key] for g in group),
                        'min_%s' % attr: min(g[attr_key] for g in group),
                        'avg_%s' % attr: avg(g[attr_key] for g in group),
                    }
                )
            else:
                club_records[club] = {
                    'total_%s' % attr: sum(g[attr_key] for g in group),
                    'max_%s' % attr: max(g[attr_key] for g in group),
                    'min_%s' % attr: min(g[attr_key] for g in group),
                    'avg_%s' % attr: avg(g[attr_key] for g in group),
                }
#                'total_winners': sum(g['round_winners'] for g in group),
#                'max_winners': max(g['round_winners'] for g in group),
#                'min_winners': min(g['round_winners'] for g in group),
#                'avg_winners': avg(g['round_winners'] for g in group),
#                'total_margins': sum(g['round_margins'] for g in group),
#                'max_margins': max(g['round_margins'] for g in group),
#                'min_margins': min(g['round_margins'] for g in group),
#                'avg_margins': avg(g['round_margins'] for g in group),
#                'total_crowds': sum(g['round_crowds'] for g in group),
#                'max_crowds': max(g['round_crowds'] for g in group),
#                'min_crowds': min(g['round_crowds'] for g in group),
#                'avg_crowds': avg(g['round_crowds'] for g in group),
#                'total_bogs': sum(g['round_bogs'] for g in group),
#                'max_bogs': max(g['round_bogs'] for g in group),
#                'min_bogs': min(g['round_bogs'] for g in group),
#                'avg_bogs': avg(g['round_bogs'] for g in group)

            # Winners bonus isn't included in tips scores from 2012 so adjust
            # total scores
            if attr == 'total':
                for g in group:
                    if g['afl_fixture__round__season'] >= 2012:
                        if g['round_winners'] == 54:
                            club_records[club]['total_total'] += 10

            round_records[season] = club_records






#def get_all_records():
#    '''
#    Return the records for each given season.
#    '''
#    season_records = {}
#    round_records = {}
#
#    # We don't have tip data for seasons before 2008
#    for season in SEASONS:
#        for club in CLUBS:
#            season_records[club] = {
#                'max_for': (0, 0),
#                'max_against': (0, 0),
#                'max_wins': 0,
#                'max_losses': 0,
#                'max_draws': 0,
#                'max_points': 0,
#                'max_percent': 0,
#                'max_winners': 0,
#                'max_winners_exact': 0,
#                'max_margins': (0, 0),
#                'max_margins_exact': 0,
#                'max_crowds': (0, 0),
#                'max_crowds_exact': 0,
#                'max_votes': (0, 0),
#                'max_votes_exact': 0,
#                'min_for': (9999, 9999),
#                'min_against': (9999, 9999),
#                'min_wins': 9999,
#                'min_losses': 9999,
#                'min_points': 9999,
#                'min_percent': 9999,
#                'min_winners': 9999,
#                'min_winners_exact': 9999,
#                'min_margins': (9999, 9999),
#                'min_margins_exact': 9999,
#                'min_crowds': (9999, 9999),
#                'min_crowds_exact': 9999,
#                'min_votes': (9999, 9999),
#                'min_votes_exact': 9999,
#            }
#            round_records[club] = {
#                'max_for': (0, 0, None),
#                'max_against': (0, 0, None),
#                'max_winners': 0,
#                'max_margins': (0, 0, None),
#                'max_crowds': (0, 0, None),
#                'max_votes': (0, 0, None),
#                'min_for': (999, 999, None),
#                'min_against': (999, 999, None),
#                'min_winners': 999,
#                'min_margins': (999, 999, None),
#                'min_crowds': (999, 999, None),
#                'min_votes': (999, 999, None),
#            }
#
#            tips = Tip.objects   \
#                .filter(club=club)   \
#                .filter(afl_fixture__round__season=season)   \
#                .filter(afl_fixture__round__is_finals=False)
#
#            totals = {}
#            score_attrs = ('winner_score', 'margin_score',
#                           'crowd_score', 'bog_score', 'total')
#
#            # We don't have tip data for seasons before 2008
#            if season.season >= 2008:
#                for tip in tips:
#                    rnd = tip.round()
#                    if not rnd in totals:
#                        totals[rnd] = {
#                            'new': {
#                                'winner_score': 0,
#                                'margin_score': 0,
#                                'crowd_score': 0,
#                                'bog_score': 0,
#                                'total': 0
#                            },
#                            'old': {
#                                'winner_score': 0,
#                                'margin_score': 0,
#                                'crowd_score': 0,
#                                'bog_score': 0,
#                                'total': 0
#                            },
#                        }
#                    for attr in score_attrs:
#                        totals[rnd]['old'][attr] += getattr(tip, attr)
#                        # The current scoring system started in 2012
#                        if rnd.season.season >= 2012:
#                            totals[rnd]['new'][attr] += getattr(tip, attr)
#                        else:
#                            if attr != 'total':
#                                value = convert_score(tip, attr)
#                                totals[rnd]['new'][attr] += value
#                            else:
#                                total = sum(
#                                    totals[rnd]['new'][a]
#                                    for a in score_attrs
#                                    if attr != 'total'
#                                )
#                                # Add winners bonus
#                                if totals[rnd]['new']['winner_score'] == 48:
#                                    total += 10
#
#                                totals[rnd]['new'][attr] += total
#
#            else:
#                # Do something with past ladders
#                pass
#
#    return {'season': season_records, 'round': round_records}


def convert_score(tip, attr):
    '''
    Convert the attr score for tip from the old scoring system to the new one.
    '''
    new_score = 0

    score = getattr(tip, attr)

    if attr == 'winner_score':
        if score:
            new_score = 6
        else:
            new_score = score

    elif attr == 'margin_score':
        if score == 40:
            new_score = 20
        elif score == 34:
            new_score = 18
        elif score == 28:
            new_score = 16
        elif score == 27:
            new_score = 14
        elif score == 21:
            new_score = 12
        elif score == 20:
            new_score = 10
        else:
            new_score = max(0, score - 5)

    elif attr == 'crowd_score':
        if score == 10:
            new_score = 8
        else:
            new_score = score

    elif attr == 'bog_score':
        new_score = score * 2 / 3

    return new_score


def legends_records():
    '''
    Get records from legends ladder.
    '''
    records = {
        'most_wins': 0,
        'least_wins': 1000,
        'most_losses': 0,
        'least_losses': 1000,
        'most_draws': 0,
        'most_for': 0,
        'least_for': 10000,
        'most_against': 0,
        'least_against': 10000,
        'most_percentage': 0.0,
        'least_percentage': 1000.0,
        'most_points': 0,
        'least_points': 1000,
    }

    for season in SEASONS:
        # We have no data at all for 2006
        if season.season == 2006:
            continue

        if season.season < 2008:
            model = PastLegendsLadder
            ladders = model.objects.filter(season=season)
        else:
            season, rounds, ladder_rounds = get_rounds(season)
            last_round = ladder_rounds.reverse()[0]
            model = LegendsLadder
            ladders = model.objects.filter(round=last_round)

        for ladder in ladders:
            value = ladder.win
            records['most_wins'] = max(records['most_wins'], value)
            records['least_wins'] = min(records['least_wins'], value)

            value = ladder.loss
            records['most_losses'] = max(records['most_losses'], value)
            records['least_losses'] = min(records['least_losses'], value)

            records['most_draws'] = max(records['most_draws'], ladder.draw)

            if season.season < 2008:
                value = ladder.points_for
            else:
                value = ladder.score_for
            records['most_for'] = max(records['most_for'], value)
            records['least_for'] = min(records['least_for'], value)

            if season.season < 2007:
                pass
            elif season.season == 2007:
                value = ladder.points_against
            else:
                value = ladder.score_against
            records['most_against'] = max(records['most_against'], value)
            records['least_against'] = min(records['least_against'], value)

            if season.season >= 2007:
                records['most_percentage'] = max(
                    records['most_percentage'],
                    ladder.percentage
                )
                records['least_percentage'] = min(
                    records['least_percentage'],
                    ladder.percentage
                )
            if season.season < 2008:
                value = ladder.score
            else:
                value = ladder.points
            records['most_points'] = max(records['most_points'], value)
            records['least_points'] = min(records['least_points'], value)

    return records
