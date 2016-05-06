"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3

Main admin data models import configurations file for the Samaritan CMA app.
"""

from django.contrib import admin
from .models import Address, Member, ChurchRole, ChurchGroup

admin.site.register(Address)
admin.site.register(Member)
admin.site.register(ChurchRole)
admin.site.register(ChurchGroup)
