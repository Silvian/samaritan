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
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django_common.auth_backends import User
from django.utils.timezone import now

from api.views import success_response, failure_response
from authentication.helpers import (
    initiate_mfa_auth,
    validate_login_token,
    validate_mfa_code,
    valid_cookie,
    set_cookie,
)
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


def passwordless_view(request):
    context = SettingsConstants.get_settings()
    return render(request, "samaritan/passwordless.html", context)


def send_login_email(request):
    if request.method == 'POST':
        if request.POST['email']:
            try:
                user = User.objects.get(email=request.POST['email'].lower())
                user.profile.send_login_email(get_current_site(request).name)
                return JsonResponse(success_response)

            except User.DoesNotExist:
                pass

            except User.MultipleObjectsReturned:
                pass

        return JsonResponse(failure_response)


def login_mfa_view(request, token):
    context = SettingsConstants.get_settings()
    if request.method == 'GET':
        return render(request, "samaritan/mfa.html", context)

    if request.method == 'POST':
        if token:
            code = request.POST['code']
            if validate_mfa_code(request, code, token):
                response = HttpResponseRedirect(settings.REDIRECT_URL)
                if request.POST.get('remember', None):
                    set_cookie(response, token)
                return response

        context['msg'] = AuthenticationConstants.INVALID_CODE
        return render(request, "samaritan/mfa.html", context)


def login_with_token(request, token):
    if request.method == 'GET':
        context = SettingsConstants.get_settings()
        if token:
            validated, redirect_url, message = validate_login_token(request, token)
            if validated:
                return HttpResponseRedirect(redirect_url)

            else:
                # the authentication system was unable to verify token
                context['msg'] = message
                return render(request, "samaritan/login.html", context)


def authenticate_user(request):
    if request.method == 'POST':
        # the password is verified for the user
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        context = SettingsConstants.get_settings()

        if not user:
            # the authentication system was unable to verify the username and password
            context['msg'] = AuthenticationConstants.INVALID_CREDENTIALS
            return render(request, "samaritan/login.html", context)

        if not user.is_active:
            context['msg'] = AuthenticationConstants.ACCOUNT_DISABLED
            return render(request, "samaritan/login.html", context)

        if not valid_cookie(user, request.COOKIES.get("mfa", None)):
            token = initiate_mfa_auth(user)
            if token:
                # mfa enabled
                redirect_url = settings.MFA_URL + token + "/"
                return HttpResponseRedirect(redirect_url)

        login(request, user)

        if user.profile.password_reset:
            return HttpResponseRedirect(settings.RESET_URL)

        if user.profile.password_breached:
            return HttpResponseRedirect(settings.RESET_URL)

        if user.profile.password_strength < settings.PASSWORD_ENTROPY_THRESHOLD:
            return HttpResponseRedirect(settings.RESET_URL)

        return HttpResponseRedirect(settings.REDIRECT_URL)


def forgot_view(request):
    context = SettingsConstants.get_settings()
    return render(request, "samaritan/forgot.html", context)


def forgot_password(request):
    if request.method == 'POST':
        if request.POST['email']:
            try:
                user = User.objects.get(email=request.POST['email'].lower())
                user.profile.send_password_email(get_current_site(request).name)
                return JsonResponse(success_response)

            except User.DoesNotExist:
                pass

            except User.MultipleObjectsReturned:
                pass

        return JsonResponse(failure_response)
    

@login_required
def reset_view(request):
    context = SettingsConstants.get_settings()
    return render(request, "samaritan/reset.html", context)


@login_required
def change_password(request):
    if request.method == 'POST':
        user = get_user(request)
        context = SettingsConstants.get_settings()

        # validate current password
        if not user.check_password(request.POST['current_password']):
            context['msg'] = AuthenticationConstants.INCORRECT_PASSWORD
            return render(request, "samaritan/reset.html", context)

        # check new password is not the same as current password
        if request.POST['new_password'] == request.POST['current_password']:
            context['msg'] = AuthenticationConstants.SAME_PASSWORD
            return render(request, "samaritan/reset.html", context)

        # check that the new password and the confirmation password are the same
        if request.POST['new_password'] != request.POST['confirm_password']:
            context['msg'] = AuthenticationConstants.PASSWORD_MISMATCH
            return render(request, "samaritan/reset.html", context)

        # validate password strength
        if not user.profile.verify_password_strength(request.POST['new_password']):
            context['msg'] = AuthenticationConstants.WEAK_PASSWORD
            return render(request, "samaritan/reset.html", context)

        # verify password has not been found in a breached database
        if user.profile.verify_password_breached(request.POST['new_password']):
            context['msg'] = AuthenticationConstants.BREACHED_PASSWORD
            return render(request, "samaritan/reset.html", context)

        user.set_password(request.POST['new_password'])
        user.profile.password_reset = False
        user.profile.password_last_updated = now()
        user.save()
        return HttpResponseRedirect(settings.REDIRECT_URL)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_URL)
