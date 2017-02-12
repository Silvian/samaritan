"""
@author: Silvian Dragan
@Date: 05/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main file for storing constants classes
"""

from django.conf import settings


class SettingsConstants:
    author = settings.AUTHOR
    copyright = settings.COPYRIGHT
    credits = settings.CREDITS
    licence = settings.LICENCE
    version = settings.VERSION
    maintainer = settings.MAINTAINER
    email = settings.EMAIL
    status = settings.STATUS

    def __init__(self):
        return

    def get_settings(self):
        return {'author': self.author, 'copyright': self.copyright,
                'credits': self.credits, 'licence': self.licence,
                'version': self.version, 'maintainer': self.maintainer,
                'email': self.email, 'status': self.status}


class WriterConstants:
    TITLE_TEXT = "Report"

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

