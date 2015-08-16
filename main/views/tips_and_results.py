# Tips and results views

import datetime
from itertools import groupby
import json
import logging
from statistics import mean

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext

from main.models import (
    Club, LegendsLadder, Round, SupercoachRanking, Tip
)
from main import constants, forms
from main.lib.footywire import Footywire
from main.utils.misc import chunks
from main.views import JSONResponse
from main.views.auth import render_auth_form

selected_page = 'tips'


@login_required
def view_tips(request, round_id):
    """
    Display the Legends tips and results for the round.

    Show results, tips and tip forms depending on the state of play. Handle tip
    submission via ajax.
    """
    if round_id:
        selected_round = Round.objects.get(id=int(round_id))
    else:
        selected_round = Round.objects.get(id=request.session['live_round'])
    request.session['selected_round'] = selected_round.id

    selected_round.set_tipping_deadline()

    games = selected_round.games.all()
    clubs = selected_round.clubs_by_games(games)

    # We want to see results, tips or tipp forms depending on the state of the
    # round
    form_games = []
    result_games = []
    tip_games = []
    for game in games:
        tips = game.tips_by_club(clubs)
        if game.status == 'Scheduled':
            if game.deadline_has_passed:
                tip_games.append((game, tips))
            else:
                form_games.append((game, tips))
        else:
            result_games.append((game, tips))
            tip_games.append((game, tips))

    # Render the round navigation buttons
    content = render_round_nav(request, selected_round)

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
        logger = logging.getLogger('legends.result')

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
            if game.game_date + delta <= now:
                # The game's result might be missing due to a problem with
                # Footywire (e.g. missing Supercoach scores) so just ignore it
                # unless it's flagged as an manual result
                try:
                    result = results[(game.afl_home.name, game.afl_away.name)]
                except KeyError:
                    if game.is_manual_result:
                        available_results.append(game)
                    continue
                if not game.is_manual_result:
                    SupercoachRanking.objects.filter(game=game).delete()
                    set_afl_result(game, result)
                available_results.append(game)

        score_types = (
            'crowds_score', 'margins_score', 'score',
            'supercoach_score', 'winners_bonus', 'winners_score'
        )

        # Set up the bye results for the round
        byes = dict((b.club, b) for b in curr_round.byes.all())
        for club in byes:
            for attr in score_types:
                setattr(byes[club], attr, 0)

        calculate_tip_scores(curr_round, games, byes)

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
        if curr_round.status == constants.Round.SCHEDULED:
            for game in available_results:
                game.status = constants.Game.PROVISIONAL
                game.save()
            curr_round.status = constants.Round.PROVISIONAL
            curr_round.set_tipping_deadline()
        elif all(g.status == constants.Game.PROVISIONAL for g in games):
            for game in games:
                game.status = constants.Game.FINAL
                game.save()
            curr_round.status = constants.Round.FINAL
            finalise_round(request, curr_round)
        else:
            curr_round.set_tipping_deadline()
        curr_round.save()

        # Log the results we got
        _log_results(available_results)

    # Redirect to the tips page when we're done
    return redirect('/legends/%s/tips/' % round_id)


def finalise_round(request, curr_round):
    """
    Set up the next round
    """

    next_round = curr_round.next_round
    if next_round:
        if next_round.is_finals:
            next_round.create_finals_fixtures()
        next_round.set_tipping_deadline()
        next_round.save()

        request.session['live_round'] = next_round.id


def render_results(request, selected_round, games):
    """
    Render all results
    """
    if not games:
        return b''

    round_values = {
        'bonus_score': [],
        'crowds_score': [],
        'margins_score': [],
        'score': [],
        'supercoach_score': [],
        'winners_score': [],
    }

    score_attrs = (
        'winners_score', 'margins_score', 'crowds_score', 'supercoach_score',
        'score'
    )

    legends_games = selected_round.games.all()
    for game in legends_games:
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
    grouped_games = chunks((g for g in legends_games), size)

    # Split byes into two chunks
    size, remainder = divmod(selected_round.num_games, 2)
    if remainder:
        size += 1
    byes = [byes[:size], byes[size:]]

    context = {
        'round': selected_round,
        'byes': byes,
        'grouped_games': grouped_games,
        'total_summary': total_summary
    }

    content = render(
        request,
        'legends_result.html',
        context
    )

    return content.content


def render_tips(request, selected_round, game_tip_data):
    """
    View tips
    """
    if not game_tip_data:
        return b''

    # Summarise tips for each game
    data = []
    games = []
    byes = selected_round.bye_clubs

    for game, tips in game_tip_data:
        # Group tips according to legends games and byes
        if byes:
            game_tips = [t for t in tips if t.club not in byes]
            bye_tips = [t for t in tips if t.club in byes]
        else:
            game_tips = tips[:]
            bye_tips = []
        game_tips = chunks(game_tips)
        games.append(game)

        if game.status == constants.Game.SCHEDULED:
            summary = tip_summary(game, tips)
        else:
            summary = tip_result_summary(game, tips)

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
        frms = create_tip_forms(selected_round, club, games=games)
        context['forms'] = frms

    # Show AFL fixtures if club hasn't paid fees yet or can't otherwise tip
    else:
        context['afl_games'] = selected_round.games

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
        logger = logging.getLogger('legends.tip')

        form[0].save()

        # Supercoach
        for frm in form[1:]:
            for f in frm:
                f.save()

        tip = form[0].instance

        # Log tip input
        log_message = '{}: {}: Winner: {} Margin: {} Crowd: {}'.format(
            tip.club,
            tip.game,
            tip.winner,
            tip.margin,
            tip.crowd
        )
        logger.info(log_message)

        for supercoach in tip.supercoach_tips.all():
            log_message = '{}: {}: Supercoach: {}'.format(
                tip.club,
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
    frms = create_tip_forms(selected_round, club, data=post_data)
    is_valid = {}
    for form in frms:
        if form[0].is_valid() \
                and all([f.is_valid() for f in form[1]]):
            # Default tips are not valid
            if form[0].instance.is_default:
                form[0].instance.is_default = False
            _save(form)
            is_valid[form[0].instance.id] = True
        else:
            is_valid[form[0].instance.id] = False
    return JSONResponse(is_valid)


# Utility functions
def create_tip_forms(selected_round, club, games=None, data=None):
    """
    Create a tip form for each tip in data.
    """
    form_list = []

    # Get all of the coach's tips for the round if we have no data
    if data is None:
        tips = [t for g in games for t in g[1] if t.club == club]
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
            player_tips = tip.supercoach_tips.all()
            tip_data = {
                '{}=winner'.format(tip.id): tip.winner,
                '{}-margin'.format(tip.id): tip.margin,
                '{}-crowd'.format(tip.id): tip.crowd
            }

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
                instance=sc
            )
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
    game.status = constants.Game.PROVISIONAL
    game.save()

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
    for score in scores:
        if previous != score['score']:
            if player_count >= 5:
                break
            rank = player_count + 1
            previous = score['score']

        sc_rank = SupercoachRanking(
            game=game,
            player=players[score['player'].lower()],
            ranking=rank
        )
        sc_rank.save()
        player_count += 1


def calculate_tip_scores(current_round, results, byes):
    """
    Calculate tip scores for the given games.
    """
    if not results:
        return

    for result in results:
        if result.status == constants.Game.SCHEDULED:
            continue

        winner = result.afl_winner
        margin = result.margin
        # The round builtin rounds half to even when we want to round half up
        crowd = 1000 * int((result.crowd + 500) / 1000)

        # We need to keep track of default tips since they get one less than the
        # lowest score for the AFL game
        default_tips = []

        # We'll never get a score this high
        lowest_score = 999

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
            if crowd:   # Allow for abandoned games
                diff = abs(tip.crowd - crowd)
                if diff in constants.TipPoints.CROWDS:
                    tip.crowds_score = constants.TipPoints.CROWDS[diff]
                else:
                    tip.crowd_score = 0
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
            tip.score = tip.winners_score + tip.margins_score +   \
                tip.crowds_score + tip.supercoach_score
            tip.save()

            lowest_score = min(lowest_score, tip.score)

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

    # Update the scores for the round
    # Include the winners bonus for home/away rounds with 9 games
    # TODO: This is a bit clunky so maybe try a query of some sort
    bonus_games = constants.TipPoints.WINNERS_BONUS_GAME_COUNT
    bonus_score = bonus_games * constants.TipPoints.WINNER

    score_types = (
        'crowds_score', 'margins_score', 'score', 'supercoach_score',
        'winners_score'
    )

    for game in results:
        for team in ('legends_home', 'legends_away'):
            club = getattr(game, team)
            is_home = team == 'legends_home'
            tips = Tip.objects \
                .filter(club=club) \
                .filter(game__round=game.round) \
                .exclude(game__status=constants.Game.SCHEDULED)
            for score_type in score_types:
                if is_home:
                    attr = 'legends_home_{}'.format(score_type)
                else:
                    attr = 'legends_away_{}'.format(score_type)
                setattr(game, attr, sum(getattr(t, score_type) for t in tips))

                # Winners bonus
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

    # Handle the byes
    for club, bye in byes.items():
        tips = Tip.objects \
            .filter(club=club) \
            .filter(game__round=game.round) \
            .exclude(game__status=constants.Game.SCHEDULED)
        for score_type in score_types:
            setattr(bye, score_type, sum(getattr(t, score_type) for t in tips))
            if bye.winners_score == bonus_score:
                bye.winners_bonus = constants.TipPoints.WINNERS_BONUS
                bye.score += game.winners_bonus
            else:
                bye.winners_bonus = 0
        bye.save()


def tip_summary(game, tips):
    """
    Build a summary of the game's tips.
    """
    summary = {}

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
    player_count = []
    players = [s.player for t in tips for s in t.supercoach_tips.all()]

    for player in set(players):
        if player is not None:
            player_count.append((player, players.count(player)))
    player_count = sorted(player_count, key=lambda x: x[1], reverse=True)

    grouped_player_count = []
    for key, group in groupby(player_count, lambda x: x[1]):
        group = sorted(list(group), key=lambda x: x[0].last_name)
        grouped_player_count.append((key, [g[0] for g in group]))

    summary['supercoach'] = grouped_player_count

    return summary


def tip_result_summary(game, tips):
    """
    Summarise results for each AFL game that has a result
    Just get minimum/maximum/average scores for each quarter
    """
    summary = {}

    score_attrs = (
        'winners_score', 'margins_score', 'crowds_score', 'supercoach_score',
        'score'
    )

    for attr in score_attrs:
        values = [getattr(t, attr) for t in tips]
        summary[attr] = {
            'max': max(values),
            'min': min(values),
            'avg': mean(values)
        }

    return summary


def create_legends_ladders(curr_round, games):
    """
    Create the Legends ladder for each club for round
    """
    ladders = curr_round.legends_ladders()
    round_ladders = []
    for game in curr_round.games.all():
        for club in (game.legends_away, game.legends_home):
            ladder = ladders[club]
            # Clear the existing ladders since we don't know which games are
            # already included
            ladder.clear()

            # Update the ladder contents
            ladder.update_columns(game)
            ladder.finalise()
            round_ladders.append(ladder)

    # If the round has byes we need to copy the previous round's ladder for the
    # affected clubs
    for bye in curr_round.byes.all():
        try:
            ladder = ladders[bye.club]
        except KeyError:
            ladder = LegendsLadder(round=curr_round, club=bye.club)

        # Clear the existing ladders since we don't know which games are
        # already included
        ladder.clear()

        # Update the ladder contents - just finalise since there's no game info
        # to worry about
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

    clubs = curr_round.season.clubs
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

            # Update the ladder contents - just finalise since there's no game info
            # to worry about
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

    for game in curr_round.games.all():
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
