"""
@author: Silvian Dragan
@Date: 07/04/2020
@Copyright: Copyright 2020, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""
from axes.models import AccessAttempt

from authentication.models import MFACode


def validate_mfa_code(code, user):
    mfa_code = MFACode.objects.filter(user=user).last()
    if mfa_code:
        if not mfa_code.expired:
            if str(code) == mfa_code.calculate_six_digit_code():
                return True

        attempt = AccessAttempt.objects.filter(username=user.username).last()
        if attempt:
            failure_count = attempt.failures_since_start + 1
            attempt.failures_since_start = failure_count
            attempt.save()
        else:
            AccessAttempt.objects.create(username=user.username, failures_since_start=1)

    return False
