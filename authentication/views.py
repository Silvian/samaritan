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
from django.contrib.auth import authenticate, login, logout
from samaritan.constants import SettingsConstants


def login_view(request):
    context = SettingsConstants.get_settings(SettingsConstants())
    if request.GET.get('logout', False):
        context['logout'] = True
        context['msg'] = "You've been logged out successfully"
    if request.GET.get('lockout', False):
        context['lockout'] = True
        context['msg'] = (
            "Your account has been locked due to repeated failed login attempts! "
            "Please contact the system administrator"
        )

    return render(request, "samaritan/login.html", context)


def authenticate_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        context = SettingsConstants.get_settings(SettingsConstants())
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(settings.REDIRECT_URL)
            else:
                context['msg'] = "This account has been disabled"
                return render(request, "samaritan/login.html", context)
        else:
            # the authentication system was unable to verify the username and password
            context['msg'] = "The username or password is incorrect"
            return render(request, "samaritan/login.html", context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_URL)
