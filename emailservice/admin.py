"""
@author: Silvian Dragan
@Date: 07/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib import admin
from .models import (
    ChurchEmailConfiguration,
    BirthdayEmailGreetingConfiguration,
    BirthdaysListConfiguration,
    GroupRotationConfiguration,
)

admin.site.register(ChurchEmailConfiguration)
admin.site.register(BirthdaysListConfiguration)
admin.site.register(BirthdayEmailGreetingConfiguration)
admin.site.register(GroupRotationConfiguration)
