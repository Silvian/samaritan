"""
This is the main views file for Samaritan CMA app

@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""

from constants import SettingsConstants
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# this loads teh main settings constants that display
# information about licence, version etc. on the footer.
footer_context = SettingsConstants.get_settings(SettingsConstants())


@login_required
def index_view(request):
    return render(request, "samaritan/index.html", footer_context)


@login_required
def members_view(request):
    return render(request, "samaritan/members.html", footer_context)


@login_required
def guests_view(request):
    return render(request, "samaritan/guests.html", footer_context)


@login_required
def everyone_view(request):
    return render(request, "samaritan/everyone.html", footer_context)


@login_required
def roles_view(request):
    return render(request, "samaritan/roles.html", footer_context)


@login_required
def historical_view(request):
    return render(request, "samaritan/history.html", footer_context)
