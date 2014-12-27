# Tips and results views

import collections
import datetime
from itertools import groupby
import logging
from statistics import mean

import numpy

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext

from main.models import (
#    Round, Bye, Points, CrowdPoints, MarginPoints, LegendsFixture, Tip,
#    LegendsLadder, FinalLadder
    Bye, Club, Game, Round, Tip,
)
from main import forms
from main.lib.footywire import Footywire
from main.utils.misc import chunks
from main.views.auth import render_auth_form

# Log tips by default
logger = logging.getLogger('tips')

selected_page = 'tips'


@login_required
def view_tips(request, round_id):
    """
    Display the Legends tips and results for the round.

    Show results, tips and tip forms depending on the state of play.
    """
    if round_id:
        selected_round = Round.objects.get(id=round_id)
    else:
        selected_round = Round.objects.get(id=request.session['live_round'])

    selected_round.set_tipping_deadline()

    form_games = []
    tip_games = []
    result_games = []
    for game in selected_round.games.all():
        if game.status == 'Scheduled':
            if game.deadline_has_passed:
                tip_games.append(game)
            else:
                form_games.append(game)
        else:
            result_games.append(game)

    # Render the round navigation buttons
    content = render_round_nav(request, selected_round)

    # Render the in progress banner
#    content += render_in_progress(request, selected_round)

    # Render tip results/tips/forms
    content += render_results(request, selected_round, result_games)
    content += render_tips(request, selected_round, tip_games)
#    content += render_tip_forms(request, selected_round, form_games)

    # Render login or change password form
    content += render_auth_form(request)

    context = {
        'content': content,
        'live_round': Round.objects.get(id=request.session['live_round']),
        'club': Club.objects.get(id=request.session['club']),
        'selected_page': selected_page,
    }
    return render_to_response(
        'main.html',
        context,
        context_instance=RequestContext(request)
    )


def render_round_nav(request, selected_round=None):
    """
    Render the round navigation buttons.
    """
    if not selected_round:
        selected_round = Round.objects.get(id=request.session['live_round'])

    season = selected_round.season

    rounds = Round.objects.filter(season=season)
    if selected_round.is_finals:
        # TODO: Check if later rounds are final
        rounds = rounds.filter(start_time__lte=selected_round.start_time)
    else:
        rounds = rounds.filter(is_finals=False)
    rounds = rounds.order_by('start_time')

    round_nav = render(
        request,
        'round_nav.html',
        {
            'selected_round': selected_round,
            'rounds': rounds
        }
    )

    return round_nav.content


def render_in_progress(request, selected_round=None):
    """
    Render the in progress banner.
    """
    if not selected_round:
        selected_round = Round.objects.get(id=request.session['live_round'])

    if selected_round.status != 'Final' and selected_round.deadline_has_passed:
        in_progress = render(
            request,
            'in_progress.html',
            {'selected_round': selected_round},
        )
        return in_progress.content

    return b''


def get_results(request, round_id):
    """
        Get fixture results and set up ladders
    """

    def _log_results(results):
        logger = logging.getLogger('results')

        for result in results:
            log_message = '%s: %s %s - %s %s (%d)' %   \
                (
                    curr_round, result.home, result.home_score,
                    result.away_score, result.away, result.crowd
                )
            logger.info(log_message)

            for bog in result.bogs.all():
                log_message = '\t%s - %s' % (bog.player, bog.votes)
                logger.info(log_message)

    curr_round = Round.objects.get(id=round_id)
    results = curr_round.aflfixtures.all()

    # Wait until 4 hours after the game is due to start to allow for slack
    # website updating:)
    all_results_provisional = all(r.status == 'Provisional' for r in results)

    if not curr_round.status == 'Final':
        # Don't get results until 4 hours after game starts
        delta = datetime.timedelta(seconds=4 * 60 * 60)
        now = datetime.datetime.today()
        available_results = []

        # Get the available AFL results
        # Start with the Footywire fixture data for the round
        # Do finals manually until I can sort out Footywire's format
        if not curr_round.is_finals:
            footywire = Footywire(curr_round)
            footywire.get_results()

        for result in results:
            if result.status == 'Scheduled':
                if result.fixture_date + delta <= now:
                    footywire.save_result(result)
                    available_results.append(result)
            else:
                available_results.append(result)

        # Set up the Legends results for the round
        legends_results = {}
        for result in curr_round.legendsfixtures.all():
            result.away_score = 0
            result.home_score = 0

            for club in (result.away, result.home):
                legends_results[club] = result

        byes = dict((b.club, b) for b in curr_round.byes.all())
        for club in byes:
            byes[club].score = 0

        calculate_tip_scores(available_results, legends_results, byes)

        # Update the ladders for home/away rounds
        if not curr_round.is_finals:
            create_legends_ladders(curr_round)
            create_afl_ladders(curr_round)
            create_streak_ladders(curr_round)

        # Update status for round
        if curr_round.status == 'Scheduled':
            curr_round.set_status('Provisional')
            curr_round.set_tipping_deadline()
        elif all_results_provisional:
            for res in results:
                res.status = 'Final'
                res.save()
            curr_round.set_status('Final')
            finalise_round(request, curr_round)
        curr_round.save()

        # Log the results we got
        _log_results(available_results)

        # Create/update a projected final ladder
        project_final_ladder(curr_round)

    # Redirect to the tips page when we're done
    return redirect('/legends/%s/tips/' % round_id)


def finalise_round(request, curr_round):
    """
    Set up the next round
    """

    next_round = curr_round.next_round()
    if next_round:
        if next_round.is_finals:
            next_round.create_finals_fixtures()
        next_round.set_tipping_deadline()
        next_round.save()

        request.session['active_round'] = next_round


def render_results(request, selected_round, games):
    """
        Render all results
    """
    if not games:
        return b''

    game_data = []
    round_values = {
        'bonus_score': [],
        'crowds_score': [],
        'margins_score': [],
        'score': [],
        'supercoach_score': [],
        'winners_score': [],
    }

    # Summarise results for each AFL game that has a result
    # Just get minimum/maximum/average scores for each quarter
    score_attrs = (
        'winners_score', 'margins_score', 'crowds_score', 'supercoach_score',
        'score'
    )

    tips_dict = selected_round.tips(games, sort_by_game=True)

    for game, tips in tips_dict.items():
        # Group tips according to legends games and byes
        bye_clubs = game.round.bye_clubs
        if bye_clubs:
            game_tips = [t for t in tips if t.club not in bye_clubs]
            bye_tips = [t for t in tips if t.club in bye_clubs]
        else:
            game_tips = tips[:]
            bye_tips = []
        game_tips = chunks(game_tips)

        game_summary = {}
        for attr in score_attrs:
            values = [getattr(t, attr) for t in tips]
            game_summary[attr] = {
                'max': max(values),
                'min': min(values),
                'avg': mean(values)
            }

        game_data.append({'game': game,
                          'game_tips': game_tips,
                          'bye_tips': bye_tips,
                          'summary': game_summary})

        # Update round scores
        for team in ('legends_away', 'legends_home'):
            for attr in score_attrs:
                _attr = '{}_{}'.format(team, attr)
                round_values[attr].append(getattr(game, _attr))
            # Winners bonus
            round_values['bonus_score'].append(game.legends_away_winners_bonus)
            round_values['bonus_score'].append(game.legends_home_winners_bonus)

    # Handle byes
    byes = selected_round.byes.all()
    if byes:
        for bye in byes:
            for attr in score_attrs:
                round_values[attr].append(getattr(bye, attr))
            # Winners bonus
            round_values['bonus_score'].append(bye.winners_bonus)

    # Total summary for the round
    total_summary = {}

    for attr in score_attrs:
        summary = {
            'max': max(round_values[attr]),
            'min': min(round_values[attr]),
            'avg': mean(round_values[attr])
        }
        total_summary[attr] = summary

        # Winners bonus
        total_summary['winners_bonus'] = {
            'max': max(round_values['bonus_score']),
            'min': min(round_values['bonus_score']),
            'avg': mean(round_values['bonus_score'])
        }

    # Split games into two chunks
    if selected_round.is_finals:
        size, remainder = divmod(selected_round.num_games, 2)
        if remainder:
            size += 1
    else:
        size = 5
    grouped_games = chunks(games, size)

    # Split byes into two chunks
    size, remainder = divmod(selected_round.num_games, 2)
    if remainder:
        size += 1
    byes = [byes[:size], byes[size:]]

    context = {
        'round': selected_round,
        'data_type': 'result',
        'games': games,
        'byes': byes,
        'grouped_games': grouped_games,
        'show_form': False,
        'data': game_data,
        'total_summary': total_summary
    }

    content = render(
        request,
        'view_tips_and_results.html',
        context
    )

    return content.content


def render_tips(request, selected_round, games):
    """
        View tips
    """
    if not games:
        return b''

#    club = Club.objects.get(id=request.session['club'])
    tips_dict = selected_round.tips(games, sort_by_game=True)

    # Summarise tips for each game
    data = []
    games = []
    for game, tips in tips_dict.items():
        # Group tips according to legends games and byes
        byes = game.round.bye_clubs
        if byes:
            game_tips = [t for t in tips if t.club not in byes]
            bye_tips = [t for t in tips if t.club in byes]
        else:
            game_tips = tips[:]
            bye_tips = []
        game_tips = chunks(game_tips)

        summary = {}

        games.append(game)

        winners = []
        summary['margin'] = []
        for club in (game.afl_home, game.afl_away):
            winners.append((club, len([t for t in tips if t.winner == club])))

            margins = [t.margin
                       for t in tips
                       if t.winner == club and t.margin is not None]

            # There will be no margins if nobody has tipped club
            if margins:
                min_max = {
                    'max': max(margins),
                    'min': min(margins),
                    'avg': mean(margins)
                }
            else:
                min_max = {'max': 0, 'min': 0, 'avg': 0}

            summary['margin'].append((club, min_max))

        num_draws = len(tips) - sum(w[1] for w in winners)
        winners.append(('draw', num_draws))
        summary['winner'] = winners

        # Crowds
        crowds = [t.crowd for t in tips if t.crowd is not None]
        min_max = {'max': max(crowds), 'min': min(crowds), 'avg': mean(crowds)}
        summary['crowd'] = min_max

        # Supercoach
        supercoach_count = []
        supercoaches = [s.player for t in tips for s in t.supercoach_tips.all()]

        for supercoach in set(supercoaches):
            if supercoach is not None:
                supercoach_count.append(
                    (supercoach, supercoaches.count(supercoach)))
        supercoach_count = sorted(
            supercoach_count, key=lambda x: x[1], reverse=True)

        grouped_supercoach_count = []
        for key, group in groupby(supercoach_count, lambda x: x[1]):
            group = sorted(list(group), key=lambda x: x[0].last_name)
            grouped_supercoach_count.append((key, [g[0] for g in group]))

        summary['supercoach'] = grouped_supercoach_count

        data.append(
            {
                'game': game,
                'game_tips': game_tips,
                'bye_tips': bye_tips,
                'summary': summary
            }
        )

    context = {
        'round': selected_round,
        'data_type': 'tip',
        'show_form': False,
        'games': games,
        'data': data,
    }
    content = render(
        request,
        'tips.html',
        context
    )

    return content.content


def render_tip_forms(request, curr_round, fixtures):
    """
        View for tip form
    """

    if not fixtures:
        return b''

    def _save(form):

        form[0].save()

        # BOGs amd emergencies
        for frm in form[1:]:
            for f in frm:
                f.save()

        # Log tip input
        tip = form[0].tip_instance

        log_message = '%s: %s: %s: Winner: %s Margin: %s Crowd: %d' % (
            tip.club,
            curr_round,
            tip.afl_fixture,
            tip.winner,
            tip.margin,
            tip.crowd
        )
        logger.info(log_message)
        for bog in tip.bogtips.all():
            log_message = '%s: %s: %s: BOG: %s' % (
                tip.club,
                curr_round,
                tip.afl_fixture,
                bog.player
            )
            logger.info(log_message)

    def _clear_errors(form):

        form[0].errors.clear()

        for frm in form[1:]:
            for f in frm:
                f.errors.clear()

    club = request.session['club']
    club_can_tip_in_round = club.can_tip_in_round(curr_round)

    context = {
        'round': curr_round,
        'club_can_tip': club_can_tip_in_round,
        'data_type': 'tip',
        'show_form': True
    }

    # Render the tip content
    if curr_round.is_finals:
        context['afl_fixtures'] = curr_round.afl_fixtures()

    if club_can_tip_in_round:
        if request.method == 'POST':
            frms = create_tip_forms(curr_round, club, fixtures, request.POST)
            context['data'] = frms

            logger = logging.getLogger('tips')
            for form in frms:
                if form[0].is_valid()   \
                        and all([b.is_valid() for b in form[1]]):
                    _save(form)

        else:
            frms = create_tip_forms(curr_round, club, fixtures)
            context['data'] = frms
    # Show AFL fixtures if club hasn't paid fees yet
    else:
        if not 'afl_fixtures' in context:
            context['afl_fixtures'] = curr_round.afl_fixtures()

    content = render_to_response(
        'tip_form.html',
        context,
        context_instance=RequestContext(request)
    )

    return content.content


# Utility functions
def create_tip_forms(curr_round, club, fixtures, data=None):
    """
        Create a tip form for each game in the round.
    """

    form_list = []

    tips = club.tips_for_round(curr_round, fixtures=fixtures)

    for tip in tips:
        clubs = (tip.afl_fixture.home, tip.afl_fixture.away)

        season = curr_round.season
        players = []

        for club in clubs:
            players.extend([p for p in club.get_players(season)])

        tip_form = forms.TipForm(
            clubs,
            data,
            prefix=tip.id,
            instance=tip
        )

        # BOG forms
        bogs = tip.bogtips.all().order_by('id')
        bog_forms = []
        for bog in bogs:
            form = forms.BogForm(
                players,
                data,
                prefix='%0d.%0d' % (tip.id, bog.id),
                instance=bog)
            bog_forms.append(form)

        form_list.append((tip_form, bog_forms))

    return form_list


def calculate_tip_scores(afl_results, legends_results, byes):
    """
        Calculate tip scores for this result.
    """

    current_round = afl_results[0].round

    legends_fixtures = {}
    winners_count = {}
    for club in legends_results:
        legends_fixtures[club] = legends_results[club]
        winners_count[club] = 0

    for club in byes:
        winners_count[club] = 0

    # Get points values
    season = current_round.season
    points_obj = Points.objects.get(season=season)
    crowd_points = CrowdPoints.objects.filter(season=season)
    margin_points = MarginPoints.objects.filter(season=season)

    for afl_result in afl_results:
        # Create lookup for BOGs
        bog_lookup = create_bog_lookup(afl_result)

        winner = afl_result.winner()
        margin = afl_result.margin()
        crowd = int(1000 * round(afl_result.crowd / 1000.0))

        default_tips = []
        tips = Tip.objects.filter(afl_fixture=afl_result)
        lowest_score = 999   # We'll never get a score this high
        for tip in tips:
            if tip.is_default:
                default_tips.append(tip)
                continue

            # Winner score
            tip.winner_score = 0
            if winner == tip.winner:
                tip.winner_score = points_obj.correct_win
                winners_count[tip.club] += 1

            # Margin score
            tip.margin_score = 0
            if tip.winner_score:
                difference = abs(tip.margin - margin)
                if winner:
                    try:
                        margin_obj = margin_points.get(difference=difference)
                        tip.margin_score = margin_obj.points
                    except MarginPoints.DoesNotExist:
                        pass

                else:
                    if tip.margin == 0:
                        tip.margin_score = margin_points.get(difference=0)

            # Crowd score
            tip.crowd_score = 0
            difference = abs(tip.crowd - crowd)
            try:
                crowd_obj = crowd_points.get(difference=difference)
                tip.crowd_score = crowd_obj.points

            except CrowdPoints.DoesNotExist:
                pass

            # BOG score
            tip.bog_score = 0
            bogs = tip.bogtips.all()
            for bog in bogs:
                if bog.player in bog_lookup:
                    tip.bog_score += points_obj.vote * bog_lookup[bog.player]

            # Total score
            tip.total = tip.winner_score + tip.margin_score +   \
                tip.crowd_score + tip.bog_score

            tip.save()

            # Update the Legends fixture
            club = tip.club
            try:
                fixture = legends_fixtures[club]
                if club == fixture.away:
                    fixture.away_score += tip.total

                else:
                    fixture.home_score += tip.total

            except KeyError:
                byes[club].score += tip.total

            lowest_score = min(lowest_score, tip.total)

        for tip in default_tips:
            # Default tips get 0 for each category but the total is the lowest
            # score for the game less 1 so that percentage isn't blown up too
            # much
            tip.winner_score = 0
            tip.margin_score = 0
            tip.crowd_score = 0
            tip.bog_score = 0
            tip.total = max(0, lowest_score - 1)
            tip.save()

            # Update legends fixture
            fixture = legends_fixtures[tip.club]
            if tip.club == fixture.away:
                fixture.away_score += tip.total
            else:
                fixture.home_score += tip.total

    # Include the winners bonus for home/away rounds
    if not current_round.is_finals:
        if current_round.num_games == 9:
            bonus = points_obj.winner_bonus
        else:
            bonus = 0

        for result in set(legends_results.values()):
            result.away_winners_bonus = 0
            result.home_winners_bonus = 0
            for club in (result.away, result.home):
                if winners_count[club] == current_round.num_games:
                    if club == result.away:
                        result.away_winners_bonus = bonus
                        legends_results[club].away_score += bonus
                    else:
                        result.home_winners_bonus = bonus
                        legends_results[club].home_score += bonus
                legends_results[club].save()

        for club, result in byes.items():
            result.winners_bonus = 0
            if winners_count[club] == current_round.num_games:
                result.winners_bonus = bonus
                result.score += bonus

            result.save()
    else:
        for result in set(legends_results.values()):
            result.save()


def create_legends_ladders(curr_round):
    """
        Create the ladders for each club for round
    """

    ladder_names = ('brownlow', 'coleman', 'crowds', 'legends', 'margins')

    round_ladders = dict((name, []) for name in ladder_names)

    tips = curr_round.tips()

    for result in curr_round.legendsfixtures.all():
        for club in (result.away, result.home):
            ladders = curr_round.club_ladders(club)

            club_tips = tips.filter(club=club)

            for name in ladder_names:
                if name == 'legends':
                    ladders[name].create(result)

                else:
                    ladders[name].create(club_tips)

                round_ladders[name].append(ladders[name])

    # Handle the byes
    for bye in curr_round.byes.all():
        ladders = curr_round.club_ladders(bye.club)

        club_tips = tips.filter(club=bye.club)

        for name in ladder_names:
            if name == 'legends':
                ladders[name].create_for_bye(bye)
            else:
                ladders[name].create(club_tips)
            round_ladders[name].append(ladders[name])

    for ladder in round_ladders.values():
        sorted_ladder = curr_round.sort_ladder(ladder, reverse=False)
        for index, row in enumerate(sorted_ladder):
            row.position = index + 1
            row.save()


def create_afl_ladders(curr_round):
    """
        Create the AFL ladders for each club for round
    """

    ladders = curr_round.afl_ladders()

    round_ladders = []

    for result in curr_round.aflfixtures.all():
        for club in (result.away, result.home):
            ladder = ladders.get(club=club)

            if result.status == 'Scheduled':
                ladder.create_for_bye(result)
            else:
                ladder.create(result)

            round_ladders.append(ladder)

    # Handle the byes
    byes = curr_round.byes.all()
    for bye in byes:
        ladder = ladders.get(club=bye.club)

        ladder.create_for_bye(result)
        round_ladders.append(ladder)

    sorted_ladder = curr_round.sort_ladder(round_ladders, reverse=False)

    for index, row in enumerate(sorted_ladder):
        row.position = index + 1
        row.save()

    # Adjust the 2013 ladder for rounds 22 and 23 to allow for Essendon's
    # transgressions. They are deemed to finish 9th.
    if curr_round.season.season == 2013   \
            and curr_round.name in ('Round 22', 'Round 23'):
        ess_ladder = curr_round.afl_ladders().get(club__name='Essendon')
        ess_pos = ess_ladder.position
        ess_ladder.position = 9
        ess_ladder.save()

        for ladder in sorted_ladder[ess_pos:9]:
            ladder.position = ess_pos
            ladder.save()
            ess_pos += 1


def create_streak_ladders(curr_round):
    """
        Create the streak ladders for each club for round
    """

    ladders = curr_round.get_streak_ladders()

    round_ladders = []

    for result in curr_round.legendsfixtures.all():
        for club in (result.away, result.home):
            ladder = ladders.get(club=club)

            if club == result.winner():
                outcome = 'W'
            elif club == result.loser():
                outcome = 'L'
            else:
                outcome = 'D'

            ladder.create(outcome)
            round_ladders.append(ladder)

    # Handle the byes
    byes = curr_round.byes.all()
    for bye in byes:
        ladder = ladders.get(club=bye.club)
        ladder.create('B')
        round_ladders.append(ladder)

    reverse = False
    sorted_ladder = curr_round.sort_ladder(round_ladders, reverse)

    for index, row in enumerate(sorted_ladder):
        row.position = index + 1
        row.save()


def create_bog_lookup(result):
    """
        Create a lookup for result BOGs.
    """

    lookup = {}

    for bog in result.bogs.all():
        lookup[bog.player] = bog.votes

    return lookup


def project_final_ladder(rnd):
    """
    Project a final ladder starting from the given round.
    """

    # Only do the projection for the home/away rounds
    if rnd.is_finals:
        return

    # It seems pointless to do a projection too early so wait until after the
    # byes
    rounds = [
        r for r in Round.objects.filter(season=rnd.season) if r.has_byes()
    ]
    if rnd.round_number() <= rounds[-1].round_number():
        return

    ### Initialise the projection
    clubs = rnd.season.clubs()

    # Get the scores we're going to base the predictions on.
    # These will be the last N completed home or away scores for each club
    # where N is the number of home/away rounds in the current season excluding
    # rounds where the club has a bye. This should even out form differences
    # over time.
    # Byes are excluded. Games from previous seasons are necesarily included.
    # TODO: We assume there's only one bye per team per season.
    N = rnd.season.round_count() - 1

    fixtures = LegendsFixture.objects   \
        .filter(
            round__start_time__lte=rnd.start_time,
            round__is_finals=False
        )   \
        .order_by('-round__start_time')

    # Get the last N for and against scores for each club
    club_scores = collections.defaultdict(dict)
    for club in clubs:
        club_fixtures = fixtures   \
            .filter(Q(home=club) | Q(away=club))[:N]
        scores_for, scores_against = get_scores(club, club_fixtures, N)

        club_scores[club] = {
            'for': scores_for,
            'against': scores_against,
        }

    ### Project the ladder and update/create the row model instances
    ladder = project_results(rnd, club_scores)

    for row in ladder:
        row_ladder, _ = FinalLadder.objects.get_or_create(
            round=rnd, club=row[0])
        for key, value in row[1].iteritems():
            setattr(row_ladder, key, value)
        row_ladder.save()


def project_results(rnd, club_scores):
    """
    Estimate all the future results and create the projected final ladder.
    """

    ladder = base_ladder(rnd)

    # Get the points for win, draw and loss
    points = Points.objects.get(season=rnd.season)

    current_round = rnd.next_round()
    while current_round.is_finals is False:
        for fixture in current_round.legendsfixtures.all():
            home = fixture.home
            away = fixture.away

            home_score, away_score = estimate_scores(fixture, club_scores)

            # Update the ladder
            if home_score > away_score:
                ladder[home]['win'] += 1
                ladder[away]['loss'] += 1
            elif home_score == away_score:
                ladder[home]['draw'] += 1
                ladder[away]['draw'] += 1
            else:
                ladder[home]['loss'] += 1
                ladder[away]['win'] += 1

            ladder[home]['score_for'] += home_score
            ladder[home]['score_against'] += away_score
            ladder[away]['score_for'] += away_score
            ladder[away]['score_against'] += home_score

            # Update club scores
            club_scores[home]['for'].appendleft(home_score)
            club_scores[home]['against'].appendleft(away_score)
            club_scores[away]['for'].appendleft(away_score)
            club_scores[away]['against'].appendleft(home_score)

        current_round = current_round.next_round()

    # Finalise the ladder
    for club, values in ladder.iteritems():
        ladder[club]['played'] =   \
            values['win'] + values['draw'] + values['loss']
        ladder[club]['points'] =   \
            values['win'] * points.ladder_win +   \
            values['draw'] * points.ladder_draw
        ladder[club]['percentage'] =   \
            100 * float(values['score_for']) / values['score_against']

    def _sort_keys(item):
        return (
            -item[1]['points'],
            -item[1]['percentage'],
            -item[1]['score_for'],
            item[0]
        )

    final_ladder = sorted(ladder.iteritems(), key=_sort_keys)

    return final_ladder


def get_scores(club, fixtures, N):
    """
    Get the club's most recent N for and against scores.
    """

    score_for = collections.deque(maxlen=N)
    score_against = collections.deque(maxlen=N)

    for f in fixtures:
        if club == f.home:
            score_for.append(f.home_score)
            score_against.append(f.away_score)
        else:
            score_for.append(f.away_score)
            score_against.append(f.home_score)

    return score_for, score_against


def base_ladder(rnd):
    """
    Get the ladder for the round.

    Just grab the attributes we need.
    """

    attrs = ('played', 'win', 'draw', 'loss', 'score_for', 'score_against',
             'points', 'percentage')

    ladders = collections.defaultdict(dict)
    for ladder in LegendsLadder.objects.filter(round=rnd):
        ladders[ladder.club] = {attr: getattr(ladder, attr) for attr in attrs}

    return ladders


def estimate_scores(fixture, club_scores, N=1000000):
    """
    Estimate the score for the given fixture and return a tuple of the home
    and away scores.

    Each score is the average of N random values drawn from the poisson
    distribution with lambda calculated as:
        * find the average of the club's for scores
        * find the average of the club's opponent's against scores
        * average these results
    """

    def _lambda(s_for, s_against):
        n = len(s_for)
        denom = float(n) * (n + 1) / 2
        avg_for = int(sum((n - w) * s for w, s in enumerate(s_for)) / denom)

        n = len(s_against)
        avg_against = int(
            sum((n - w) * s for w, s in enumerate(s_against)) / denom
        )

        return int((avg_for + avg_against) / 2.0)

    s_for = club_scores[fixture.home]['for']
    s_against = club_scores[fixture.away]['against']
    lamb = _lambda(s_for, s_against)
    home_score = int(sum(numpy.random.poisson(lamb, N)) / float(N))

    s_for = club_scores[fixture.away]['for']
    s_against = club_scores[fixture.home]['against']
    lamb = _lambda(s_for, s_against)
    away_score = int(sum(numpy.random.poisson(lamb, N)) / float(N))

    return (home_score, away_score)
