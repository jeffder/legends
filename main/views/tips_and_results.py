# Tips and results views

import collections
import datetime
from itertools import groupby
import json
import logging
from statistics import mean

import numpy

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext

from main.models import (
#    Round, Bye, Points, CrowdPoints, MarginPoints, LegendsFixture, Tip,
#    LegendsLadder, FinalLadder
    Club, Round, SupercoachRanking, Tip
)
from main import constants, forms
from main.lib.footywire import Footywire
from main.utils.misc import chunks
from main.views import JSONResponse
from main.views.auth import render_auth_form

# Log tips by default
logger = logging.getLogger('tips')

selected_page = 'tips'


@login_required
def view_tips(request, round_id):
    """
    Display the Legends tips and results for the round.

    Show results, tips and tip forms depending on the state of play. Handle tip
    submission via ajax.
    """
    if round_id:
        selected_round = Round.objects.get(id=round_id)
    else:
        selected_round = Round.objects.get(id=request.session['live_round'])
    request.session['selected_round'] = selected_round.id

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
    content += render_tip_forms(request, selected_round, form_games)

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
                    curr_round, result.afl_home, result.afl_home_score,
                    result.afl_away_score, result.afl_away, result.crowd
                )
            logger.info(log_message)

            for sc in result.supercoach_rankings.all():
                log_message = '\t%s - %s' % (sc.player, sc.ranking)
                logger.info(log_message)

    curr_round = Round.objects.get(id=round_id)
    games = curr_round.games.all()

    if not curr_round.status == 'Final':
        # Wait until 4 hours after the game is due to start to allow for slack
        # website updating:)
        delta = datetime.timedelta(seconds=4 * 60 * 60)
        now = datetime.datetime.today()
        available_results = []

        # Get the available AFL results
        # Start with the Footywire fixture data for the round
        # Do finals manually until I can sort out Footywire's format
        if curr_round.is_finals:
            return

        footywire = Footywire(curr_round)
        results = footywire.get_results()

        for game in games:
            # This picks up all of the available results so we'll be refreshing
            # results we already have. This is intentional since something might
            # have changed since the last time we got results (usually this will
            # be supercoach rankings and adding previously missing crowds). As a
            # consequence, we need to initialise the legends scores again and
            # clear the Supercoach ranking table
            game.initialise_legends_scores()
            SupercoachRanking.objects.filter(game=game).delete()

            if game.game_date + delta <= now:
                result = results[(game.afl_home.name, game.afl_away.name)]
                set_afl_result(game, result)
                available_results.append(game)

        # Set up the bye results for the round
        byes = dict((b.club, b) for b in curr_round.byes.all())
        for club in byes:
            byes[club].score = 0

        calculate_tip_scores(curr_round, available_results)

        # Update the ladders for home/away rounds
        if not curr_round.is_finals:
            # We need all games for the round for the legends ladder because we
            # will have legends scores for games where the actual AFL game
            # hasn't been played yet. We can ignore byes because they don't
            # affect the ladder.
            create_legends_ladders(curr_round, games)
            create_non_premiership_ladders(curr_round, available_results)
            create_afl_ladders(curr_round, available_results)
            create_streak_ladders(curr_round, available_results)

        # Update status for round
        if curr_round.status == 'Scheduled':
            for res in results:
                res.status = 'Provisional'
                res.save()
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
#        project_final_ladder(curr_round)

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

    tips_dict = selected_round.tips_by_game(games)

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
    elif selected_round.has_byes:
        size, remainder = divmod(len(selected_round.bye_clubs), 2)
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
    tips_dict = selected_round.tips_by_game(games)   #, sort_by_game=True)

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
        if crowds:
            min_max = {
                'max': max(crowds), 'min': min(crowds), 'avg': mean(crowds)}
        else:
            min_max = {'max': 0, 'min': 0, 'avg': 0}
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


def render_tip_forms(request, selected_round, games=None):
    """
    View for tip form
    """
    if not games:
        return b''

    club = Club.objects.get(id=request.session['club'])
    club_can_tip = club in selected_round.tipping_clubs

    context = {
        'round': selected_round,
        'club_can_tip': club_can_tip,
        }

    if club_can_tip:
        # Post data is handled via Ajax in submit_tips()
        frms = create_tip_forms(selected_round, club)
        context['forms'] = frms

    # Show AFL fixtures if club hasn't paid fees yet or can't otherwise tip
    else:
        context['afl_games'] = selected_round.games()

    content = render_to_response(
        'tip_form.html',
        context,
        context_instance=RequestContext(request)
    )

    return content.content


def submit_tips(request):
    """
    View for handling tip submission.
    """

    def _save(form):

        form[0].save()

        # Supercoach
        for frm in form[1:]:
            for f in frm:
                f.save()

        # Log tip input
        tip = form[0].instance

        log_message = '%s: %s: %s: Winner: %s Margin: %s Crowd: %d' % (
            tip.club,
            selected_round,
            tip.game,
            tip.winner,
            tip.margin,
            tip.crowd
        )
        logger.info(log_message)
        for supercoach in tip.supercoach_tips.all():
            log_message = '%s: %s: %s: BOG: %s' % (
                tip.club,
                selected_round,
                tip.game,
                supercoach.player
            )
            logger.info(log_message)

    def _parse_post_data(request):
        """
        The keys in the post data include the form prefix so we need to clean
        them up and group them by tip.
        """
        field_data = json.loads(request.body.decode(request.encoding))

        # Group post items by tip
        form_data = {}
        for tip_id, data in field_data.items():
            tip = Tip.objects.get(id=int(tip_id))

            tip_data = {}
            # Finals rounds have more than one supercoach tip
            players = {}

            for key, value in data.items():
                if key.endswith('player'):
                    players[key] = value
                else:
                    tip_data[key] = value
            tip_data['players'] = players
            form_data[tip] = tip_data

        return form_data

    # We should get here only if we have an ajax request and the coach can tip.
    # But just in case someone does something interesting...
    selected_round = Round.objects.get(id=request.session['selected_round'])
    club = Club.objects.get(id=request.session['club'])
    club_can_tip = club in selected_round.tipping_clubs

    if not (request.method == 'POST' and request.is_ajax() and club_can_tip):
        return HttpResponseNotFound(
            'The requested page does not exist: {}'.format(request.path_info))

    # Process the form
    post_data = _parse_post_data(request)
    frms = create_tip_forms(selected_round, club, post_data)
    is_valid = {}
    for form in frms:
        if form[0].is_valid()   \
                and all([f.is_valid() for f in form[1]]):
            _save(form)
            is_valid[form[0].instance.id] = True
        else:
            is_valid[form[0].instance.id] = False

    return JSONResponse(is_valid)


# Utility functions
def create_tip_forms(selected_round, club, data=None):
    """
    Create a tip form for each tip in data.
    """
    form_list = []

    # Get all of the coach's tips for the round if we have no data
    print('data =', data)
    if data is None:
        tips = selected_round.club_tips(club)
    else:
        tips = data.keys()

    for tip in tips:
        players = []
        for club in (tip.game.afl_home, tip.game.afl_away):
            players.extend(
                club.players.filter(season=selected_round.season)
            )

        if data is not None:
            player_tips = data[tip].pop('players')
            tip_data = data[tip]
        else:
            player_tips = None
            tip_data = None

        tip_form = forms.TipForm(
            tip_data,
            prefix=tip.id,
            instance=tip
        )

        # Supercoach forms
        supercoach_forms = []
        for sc in tip.supercoach_tips.all():
            if data is not None:
                key = '{}-{}-player'.format(tip.id, sc.id)
                sc_data = {key: player_tips[key]}
            else:
                sc_data = None

            form = forms.SupercoachForm(
                players,
                sc_data,
                prefix='%0d-%0d' % (tip.id, sc.id),
                instance=sc)
            supercoach_forms.append(form)

        form_list.append((tip_form, supercoach_forms))

    return form_list


def set_afl_result(game, result):
    """
    Set the AFL game's result. We don't save the game here since we're going
    to be updating the game's tip scores later.
    """
    game.afl_home_score = result['home_score']
    game.afl_away_score = result['away_score']
    game.crowd = result['crowd']
    game.status = 'Provisional'

    # Save the Supercoach scores and rankings
    save_supercoach_results(game, result['sc_scores'])


def save_supercoach_results(game, results):
    """
    Save the Supercoach scores.
    """
    curr_round = game.round

    # Save all Supercoach scores
    players = {}
    sc_scores = []
    for club_name in results.keys():
        club = Club.objects.get(name=club_name)
        players.update({
            p.supercoach_name.lower(): p for p in club.players_by_season(
                curr_round.season
            )
        })
        sc_scores.extend(results[club_name])

    scores = reversed(sorted(sc_scores, key=lambda x: x['score']))

    # Get the top 5 scoring players in the game and rank from 5 down to 1.
    # Due to ties we might get more than 5 players
    player_count = 0
    previous = 0
    rank = 5
    for score in scores:
        if previous != score['score']:
            rank = 5 - player_count
            if rank <= 0:
                break
            previous = score['score']

        sc_rank = SupercoachRanking(
            game=game,
            player=players[score['player'].lower()],
            ranking=rank
        )
        sc_rank.save()
        player_count += 1


def calculate_tip_scores(current_round, results):
    """
    Calculate tip scores for the given games.
    """
    if not results:
        return

    # Initialise the game scores for each club. We need to map clubs to the
    # game they're playing in or bye so that we can update game scores with
    # tip scores when they're calculated. As well as the game, we also need
    # to know whether they're the home or away team or if they've got a bye
    # in this round
    club_games = {}

    score_types = (
        'crowds_score', 'margins_score', 'score', 'supercoach_score',
        'winners_score'
    )

    games = current_round.games.all()
    for game in games:
        club_games[game.legends_away] = (game, False, False)
        club_games[game.legends_home] = (game, True, False)
        for score_type in score_types:
            setattr(game, 'legends_away_{}'.format(score_type), 0)
            setattr(game, 'legends_home_{}'.format(score_type), 0)

    # Add the byes
    for bye in current_round.byes.all():
        club_games[bye.club] = (bye, False, True)
        for score_type in score_types:
            setattr(bye, score_type, 0)

    for result in results:
        winner = result.afl_winner
        margin = result.margin
        crowd = int(1000 * round(result.crowd / 1000.0))

        # We need to keep track of default tips since they get one less than the
        # lowest score for the AFL game
        default_tips = []

        # We'll never get a score this high
        lowest_score = 999

        score_types = (
            'crowds_score', 'margins_score', 'score', 'supercoach_score',
            'winners_score'
        )

        # Create lookup for the top ranked Supercoach players in game
        sc_lookup = {
            sc.player: constants.TipPoints.SUPERCOACH[sc.ranking]
            for sc in result.supercoach_rankings.filter(game=result)
        }

        # Calculate scores for each tip
        tips = result.tips.all()
        for tip in tips:
            if tip.is_default:
                default_tips.append(tip)
                continue

            # Winner and margins scores
            if winner == tip.winner:
                tip.winners_score = constants.TipPoints.WINNER

                diff = abs(tip.margin - margin)
                if diff in constants.TipPoints.MARGINS:
                    tip.margins_score = constants.TipPoints.MARGINS[diff]
                else:
                    tip.margins_score = 0
            else:
                tip.winners_score = 0
                tip.margins_score = 0

            # Crowd score
            diff = abs(tip.crowd - crowd)
            if diff in constants.TipPoints.CROWDS:
                tip.crowds_score = constants.TipPoints.CROWDS[diff]
            else:
                tip.crowd_score = 0

            # Supercoach score
            tip.supercoach_score = 0
            for sc in tip.supercoach_tips.all():
                if sc.player in sc_lookup:
                    sc.score = sc_lookup[sc.player]
                    tip.supercoach_score += sc.score
                else:
                    sc.score = 0
                sc.save()

            # Total score
            tip.total = tip.winners_score + tip.margins_score +   \
                tip.crowds_score + tip.supercoach_score
            tip.save()

            # Update the round scores
            game, is_home, is_bye = club_games[tip.club]
            for score_type in score_types:
                if is_bye:
                    attr = score_type
                else:
                    if is_home:
                        attr = 'legends_home_{}'.format(score_type)
                    else:
                        attr = 'legends_away_{}'.format(score_type)
                setattr(
                    game, attr, getattr(game, attr) + getattr(tip, score_type))

            lowest_score = min(lowest_score, tip.total)

        for tip in default_tips:
            # Default tips get 0 for each category but the total is the lowest
            # score for the game less 1 so that percentage isn't blown up too
            # much
            tip.winners_score = 0
            tip.margins_score = 0
            tip.crowds_score = 0
            tip.supercoach_score = 0
            tip.score = max(0, lowest_score - 1)
            tip.save()

            # Update round scores. We don't need to worry about anything except
            # the total score
            game, is_home, is_bye = club_games[tip.club]
            if is_bye:
                game.score += tip.score
            else:
                if is_home:
                    game.legends_home_score += tip.score
                else:
                    game.legends_away_score += tip.score

    # Include the winners bonus for home/away rounds with 9 games
    bonus_games = constants.TipPoints.WINNERS_BONUS_GAME_COUNT
    if not current_round.is_finals and current_round.num_games == bonus_games:
        bonus_score = bonus_games * constants.TipPoints.WINNER

        for game, is_home, is_bye in club_games.values():
            if is_bye:
                if game.winners_score == bonus_score:
                    game.winners_bonus = constants.TipPoints.WINNERS_BONUS
                    game.score += game.winners_bonus
                else:
                    game.winners_bonus = 0
            else:
                if is_home:
                    if game.legends_home_winners_score == bonus_score:
                        game.legends_home_winners_bonus = constants.TipPoints.WINNERS_BONUS
                        game.legends_home_score += game.legends_home_winners_bonus
                    else:
                        game.legends_home_winners_bonus = 0
                else:
                    if game.legends_away_winners_score == bonus_score:
                        game.legends_away_winners_bonus = constants.TipPoints.WINNERS_BONUS
                        game.legends_away_score += game.legends_away_winners_bonus
                    else:
                        game.legends_away_winners_bonus = 0

            game.save()
    else:
        for game, is_home, is_bye in club_games.values():
            if is_bye:
                game.winners_bonus = 0
            else:
                if is_home:
                    game.legends_home_winners_bonus = 0
                else:
                    game.legends_away_winners_bonus = 0

            game.save()


def create_legends_ladders(curr_round, games):
    """
    Create the Legends ladder for each club for round
    """
    print('Creating Legendsa ladders')
    ladders = curr_round.legends_ladders()

    round_ladders = []

    for game in games:
        for club in (game.legends_away, game.legends_home):
            ladder = ladders[club]
            # Clear the existing ladders since we don't know which games are
            # already included
            ladder.clear()

            # Update the ladder contents
            ladder.update_columns(game)
            ladder.finalise()
            round_ladders.append(ladder)

    sorted_ladder = curr_round.sort_ladder(round_ladders, reverse=False)
    for index, row in enumerate(sorted_ladder):
        row.position = index + 1
        row.save()


def create_non_premiership_ladders(curr_round, games):
    """
    Create the non-premiership Legends ladders for each club for round
    """
    ladder_names = ('brownlow', 'coleman', 'crowds', 'margins')
    round_ladders = dict((name, []) for name in ladder_names)

    clubs = curr_round.tipping_clubs
    tips = curr_round.tips_by_club(games)

    for club in clubs:
        ladders = curr_round.club_ladders(club)
        del ladders['legends']

        # Clear the existing ladders since we don't know which games are already
        # included
        for ladder in ladders.values():
            ladder.clear()

        # Update the ladder contents
        for tip in tips[club]:
            for ladder in ladders.values():
                ladder.update_columns(tip)

        for name, ladder in ladders.items():
            ladder.finalise()
            round_ladders[name].append(ladder)

    for ladder in round_ladders.values():
        sorted_ladder = curr_round.sort_ladder(ladder, reverse=False)
        for index, row in enumerate(sorted_ladder):
            row.position = index + 1
            row.save()


def create_afl_ladders(curr_round, games):
    """
    Create the AFL ladder for each club for round
    """

    ladders = curr_round.afl_ladders()

    round_ladders = []

    for game in games:
        for club in (game.afl_away, game.afl_home):
            ladder = ladders[club]
            # Clear the existing ladders since we don't know which games are
            # already included
            ladder.clear()

            # Update the ladder contents
            ladder.update_columns(game)
            ladder.finalise()
            round_ladders.append(ladder)

    # If there are still games to be played in the round or the round has byes,
    # we need to copy the previous round's ladder for the affected clubs
    played = [r.club for r in round_ladders]
    for ladder in ladders.values():
        if ladder.club not in played:
            # Clear the existing ladders since we don't know which games are
            # already included
            ladder.clear()

            # Update the ladder contents
            ladder.finalise()
            round_ladders.append(ladder)

    sorted_ladder = curr_round.sort_ladder(round_ladders, reverse=False)
    for index, row in enumerate(sorted_ladder):
        row.position = index + 1
        row.save()


def create_streak_ladders(curr_round, games):
    """
    Create the streak ladders for each club for round
    """
    ladders = curr_round.get_streak_ladders()
    round_ladders = []

    for game in games:
        for club in (game.legends_away, game.legends_home):
            ladder = ladders[club]

            if club == game.legends_winner:
                outcome = 'W'
            elif club == game.legends_loser:
                outcome = 'L'
            else:
                outcome = 'D'

            ladder.create(outcome)
            round_ladders.append(ladder)

    # Handle the byes
    byes = curr_round.byes.all()
    for bye in byes:
        ladder = ladders[bye.club]
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
    rounds = [r for r in Round.objects.filter(season=rnd.season) if r.has_byes]
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
