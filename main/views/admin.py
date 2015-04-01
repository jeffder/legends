# Admin views for superuser use only

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from main.forms import LoginForm, ChangePasswordForm, ClubSelectionForm
from main.models import Club, Round
from main.views import tips_and_results


# Log tips by default
logger = logging.getLogger('tips')

selected_page = 'admin'
selected_tab = 'manual_tips'


@login_required
def view_admin(request, **kwargs):
    """
    Display the various superuser views (only manual tips for now).
    """
    view = render_manual_tips(request, **kwargs)

    admin_nav = render_admin_nav(request, 'manual_tips')

    auth_form = tips_and_results.render_auth_form(request)

    content = admin_nav + view + auth_form

    return render_to_response(
        'main.html',
        {'content': content,
         'live_round': Round.objects.get(id=request.session['live_round']),
         'club': Club.objects.get(id=request.session['club']),
         'selected_page': selected_page,
         'selected_tab': selected_tab, },
        context_instance=RequestContext(request)
    )


def render_admin_nav(request, active_admin):
    """
    Render the admin nav.
    """

    admin_nav = render(
        request,
        'admin_nav.html',
        {'active_admin': active_admin},
    )

    return admin_nav.content


def render_manual_tips(request, **kwargs):
    """
    View for manual tips form
    """
    def _save(form):
        form[0].save()

        # BOGs
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
        logger = logging.getLogger('tips')
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

    curr_round = Round.objects.get(id=request.session['live_round'])

    games = curr_round.games.all()
    clubs = [c for c in curr_round.tipping_clubs]

    context = {
        'round': curr_round,
        'games': games,
    }

    # Render the content
    if request.method == 'POST':
        # Did we select a new club?
        if 'club' in request.POST:
            club = Club.objects.get(id=int(request.POST['club']))

            frms = tips_and_results.create_tip_forms(
                curr_round, club)
            context['data'] = frms
            request.session['manual_user'] = club.id
        # Tips submitted
        else:
            club = Club.objects.get(id=request.session['manual_user'])

            frms = tips_and_results.create_tip_forms(
                curr_round, club, request.POST)
            context['data'] = frms
            for form in frms:
                if form[0].is_valid()   \
                        and all([b.is_valid() for b in form[1]]):
                    _save(form)

        club_form = render_club_selector(
            request, curr_round=curr_round, club=club, clubs=clubs)
    else:
        club = Club.objects.get(id=request.session['club'])
        club_form = render_club_selector(
            request, curr_round=curr_round, club=club, clubs=clubs)
        frms = tips_and_results.create_tip_forms(curr_round, club)
        context['data'] = frms

    content = render_to_response(
        'manual_tips.html',
        context,
        context_instance=RequestContext(request)
    )

    return club_form + content.content


def render_club_selector(request, curr_round, club, clubs):
    """
    Render the coach selector for the manual tips form.
    """

    form = ClubSelectionForm(
        curr_round=curr_round, club=club, clubs=clubs)
    url = '/legends/admin/manual_tips/{}/'.format(club.id)

    rendered = render(
        request,
        'club_selection.html',
        {'form': form,
         'url': url}
    )

    return rendered.content


def render_auth_form(request):
    """
    Render the login form or change password form dependng on whether or not
    the user is logged in.
    """

    if request.user.is_authenticated():
        content = render(
            request,
            'accounts/change_password.html',
            {'change_password_form': ChangePasswordForm(request.user)}
        )
    else:
        content = render(
            request,
            'accounts/login.html',
            {'login_form': LoginForm()}
        )

    return content.content
