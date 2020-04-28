"""
@author: Silvian Dragan
@Date: 07/04/2020
@Copyright: Copyright 2020, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from datetime import datetime

from axes.models import AccessAttempt
from axes.utils import reset
from django.conf import settings
from django.contrib.auth import login

from authentication.models import MFACode, MFAConfiguration, MFACookie
from messageservice.tasks import send_sms_task


def initiate_mfa_auth(user):
    """use to initiate mfa auth for the request user."""
    mfa_config = MFAConfiguration.load()
    if mfa_config and mfa_config.active:
        if user.profile.mobile_number and user.profile.mfa_enabled:
            # generate the mfa code and send sms to the user
            mfa_code = MFACode.objects.create(user=user)
            message = "One time code: {}".format(mfa_code.calculate_six_digit_code())
            send_sms_task.delay(
                message=message,
                phone=user.profile.mobile_number,
            )
            return str(mfa_code.token)


def validate_mfa_code(request, code, token):
    """use to validate received mfa code against request user."""
    mfa_code = MFACode.objects.filter(token=token).last()
    if mfa_code:
        user = mfa_code.user
        if not mfa_code.expired:
            if str(code) == mfa_code.calculate_six_digit_code():
                login(request, user)
                return True

        # record failure attempts to deactivate the user account
        attempt = AccessAttempt.objects.filter(username=user.username).last()
        if attempt:
            failure_count = attempt.failures_since_start + 1
            attempt.failures_since_start = failure_count
            attempt.save()
        else:
            AccessAttempt.objects.create(username=user.username, failures_since_start=1)

    return False


def reset_user_access(user):
    """reset user access attempts used when user is activated."""
    reset(username=user.username)

    mfa_codes = MFACode.objects.filter(user=user)
    if mfa_codes:
        path_list = []
        for code in mfa_codes:
            path = settings.MFA_URL + str(code.token) + '/'
            path_list.append(path)

        # delete all records in the access attempt table
        AccessAttempt.objects.filter(path_info__in=path_list).delete()


def set_cookie(response, token):
    """set cookie if mfa is valid and device is trusted."""
    code = MFACode.objects.get(token=token)
    cookie = MFACookie.objects.create(user=code.user)
    expires = datetime.strftime(cookie.expiry_date, "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        "mfa",
        cookie.id,
        expires=expires,
        max_age=settings.COOKIE_EXPIRY_THRESHOLD,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE,
    )


def valid_cookie(user, cookie):
    """Verify cookie is set and valid for given user."""
    try:
        cookie = MFACookie.objects.get(id=cookie, user=user)
        if not cookie.expired:
            return True

    except MFACookie.DoesNotExist:
        pass

    return False
