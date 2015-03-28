# Index view

import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from main.models import Round, Season
from main.views.auth import render_auth_form


active_page = 'tips'


def index(request):
    """
    Render the index page
    """
    today = datetime.datetime.today()
    year = today.year

    while True:
        try:
            season = Season.objects.get(season=year)
            break
        except Season.DoesNotExist:
            year -= 1

    request.session['live_season'] = season.season

    live_round = season.live_round
    request.session['live_round'] = live_round.id

    # Set the tipping deadline - needed for "split" rounds and rounds with games
    # played on days other than Friday, Saturday or Sunday
    live_round.set_tipping_deadline()

    if request.user.is_authenticated():
        club = request.user.clubs.all()[0]
        request.session['club'] = club.id

        return redirect('%s/tips/' % live_round.id)
    else:
        request.session['club'] = None
        context = {
            'content': render_auth_form(request),
            'live_round': live_round,
            'selected_page': active_page
        }

        return render_to_response(
            'main.html',
            context,
            context_instance=RequestContext(request)
        )


def obj_from_id(model, id):
    """
    Get a model instance given its id.
    """
    return model.objects.get(id=id)


def view_deadline(request):
    """
        Render the tipping deadline
    """
    return render_to_response(
        'deadline.html',
        {'current_round': obj_from_id(Round, request.session['live_round'])},
        context_instance=RequestContext(request)
    )
