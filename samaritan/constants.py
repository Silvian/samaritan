"""
@author: Silvian Dragan
@Date: 05/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main file for storing constants classes
"""

from django.conf import settings
from django.utils.timezone import now


class SettingsConstants:
    """Settings constants."""

    author = settings.AUTHOR
    copyright = settings.COPYRIGHT.format(year=now().year)
    licence = settings.LICENCE
    version = settings.VERSION
    maintainer = settings.MAINTAINER
    email = settings.EMAIL

    def __init__(self):
        return

    @classmethod
    def get_settings(cls):
        return {
            'author': cls.author,
            'copyright': cls.copyright,
            'licence': cls.licence,
            'version': cls.version,
            'maintainer': cls.maintainer,
            'email': cls.email,
        }


class WriterConstants:
    """Writer constants."""

    FIRST_NAME = "First Name"
    LAST_NAME = "Last Name"
    DATE_OF_BIRTH = "Date of Birth"
    TELEPHONE = "Telephone"
    EMAIL = "Email"

    ADDRESS_NO = "No."
    ADDRESS_STREET = "Street"
    ADDRESS_LOCALITY = "Locality"
    ADDRESS_CITY = "City"
    ADDRESS_POSTCODE = "Postcode"

    DETAILS = "Details"
    IS_BAPTISED = "Is Baptised"
    BAPTISMAL_DATE = "Baptismal Date"
    BAPTISMAL_PLACE = "Baptismal Place"
    IS_MEMBER = "Is Member"
    MEMBERSHIP_TYPE = "Membership Type"
    MEMBERSHIP_DATE = "Membership Date"
    IS_ACTIVE = "Is Active"
    GDPR = "GDPR"
    CHURCH_ROLE = "Church Role"
    NOTES = "Notes"

    YES = "Yes"
    NO = "No"
    NOT_APPLICABLE = "N/A"
    NOT_SPECIFIED = "Not specified"

    DATE_FORMAT = "%d-%m-%Y"
    FILE_NAME_DATE = "%Y-%m-%d-%H.%M.%S"

    def __init__(self):
        return


class AuthenticationConstants:
    """Authentication constants."""

    LOGOUT_SUCCESS = "You've been logged out successfully"
    ACCOUNT_DISABLED = "This account has been disabled"
    INVALID_CREDENTIALS = "The username or password is incorrect"
    INVALID_CODE = "The code entered is invalid"
    LOCKOUT_MESSAGE = (
        "Your account has been locked due to repeated failed login attempts! "
        "Please contact the system administrator"
    )
    INCORRECT_PASSWORD = "Your current password is incorrect"
    PASSWORD_MISMATCH = "The new password did not match password confirmation"
    SAME_PASSWORD = "The new password cannot be the same as existing password"
    WEAK_PASSWORD = "The password is too weak and cannot be used"
    BREACHED_PASSWORD = "The password has been breached and cannot be used"

    def __init__(self):
        return
