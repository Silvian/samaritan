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

