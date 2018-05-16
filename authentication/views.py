"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Authentication module is fully completed.
Do not change anything here unless you really know what you're doing.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, get_user, login, logout
from django.utils.timezone import now

from samaritan.constants import SettingsConstants, AuthenticationConstants


def login_view(request):
    context = SettingsConstants.get_settings()
    if request.GET.get('logout', False):
        context['logout'] = True
        context['msg'] = AuthenticationConstants.LOGOUT_SUCCESS
    if request.GET.get('lockout', False):
        context['lockout'] = True
        context['msg'] = AuthenticationConstants.LOCKOUT_MESSAGE

    return render(request, "samaritan/login.html", context)


def authenticate_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        context = SettingsConstants.get_settings()
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                if user.profile.password_reset:
                    return HttpResponseRedirect(settings.RESET_URL)
                return HttpResponseRedirect(settings.REDIRECT_URL)
            else:
                context['msg'] = AuthenticationConstants.ACCOUNT_DISABLED
                return render(request, "samaritan/login.html", context)
        else:
            # the authentication system was unable to verify the username and password
            context['msg'] = AuthenticationConstants.INVALID_CREDENTIALS
            return render(request, "samaritan/login.html", context)


@login_required
def reset_view(request):
    context = SettingsConstants.get_settings()
    return render(request, "samaritan/reset.html", context)


@login_required
def change_password(request):
    if request.method == 'POST':
        user = get_user(request)
        context = SettingsConstants.get_settings()
        if user.check_password(request.POST['current_password']):
            if request.POST['new_password'] != request.POST['current_password']:
                if request.POST['new_password'] == request.POST['confirm_password']:
                    user.set_password(request.POST['new_password'])
                    user.profile.password_reset = False
                    user.profile.password_last_updated = now()
                    user.save()
                    return HttpResponseRedirect(settings.REDIRECT_URL)
                else:
                    context['msg'] = AuthenticationConstants.PASSWORD_MISMATCH
                    return render(request, "samaritan/reset.html", context)
            else:
                context['msg'] = AuthenticationConstants.SAME_PASSWORD
                return render(request, "samaritan/reset.html", context)
        else:
            context['msg'] = AuthenticationConstants.INCORRECT_PASSWORD
            return render(request, "samaritan/reset.html", context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_URL)
