"""
@author: Silvian Dragan
@Date: 07/04/2020
@Copyright: Copyright 2020, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""
from axes.models import AccessAttempt

from authentication.models import MFACode, MFAConfiguration
from messageservice.tasks import send_sms_task


def initiate_mfa_auth(user):
    """use to initiate mfa auth for the request user."""
    mfa_config = MFAConfiguration.load()
    if mfa_config and mfa_config.active:
        if user.profile.mobile_number and user.profile.mfa_enabled:
            # generate the mfa code and send sms to the user
            mfa_code = MFACode.objects.create(user=user)
            send_sms_task.delay(
                message=mfa_code.calculate_six_digit_code(),
                phone=user.profile.mobile_number,
            )
            return True

    return False


def validate_mfa_code(code, user):
    """use to validate received mfa code against request user."""
    mfa_code = MFACode.objects.filter(user=user).last()
    if mfa_code:
        if not mfa_code.expired:
            if str(code) == mfa_code.calculate_six_digit_code():
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
