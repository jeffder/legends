# Authorisation views


import json

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from main.forms import LoginForm, ChangePasswordForm


def render_auth_form(request):
    '''
    Render the login form or change password form dependng on whether or not
    the user is logged in.
    '''

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


class JSONResponse(HttpResponse):

    def __init__(self, data):
        HttpResponse.__init__(
            self, content=json.dumps(data), mimetype='application/json')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if request.is_ajax():
            if form.is_valid():
                auth_login(request, form.get_user())
                data = {'logged_in': True}
            else:
                data = {
                    'logged_in': False,
                    'errors': {
                        k: [e for e in v] for k, v in form.errors.items()}
                }

            return JSONResponse(data)

    form = LoginForm()
    data = {
        'logged_in': False,
    }

    return JSONResponse(data)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if request.is_ajax():
            if form.is_valid():
                form.save()
                data = {'changed': True}
            else:
                data = {
                    'changed': False,
                    'errors': dict([(k, [unicode(e) for e in v])
                                    for k, v in form.errors.items()])
                }

            return JSONResponse(data)


def logout(request):
    auth_logout(request)

    return redirect('/legends/')
