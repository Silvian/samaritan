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
from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
from models import Member, ChurchRole, Address
from forms import AddMemberForm
import json

# this loads teh main settings constants that display
# information about licence, version etc. on the footer.
footer_context = SettingsConstants.get_settings(SettingsConstants())
success_response = {'success': True}


@login_required
def index_view(request):
    return render(request, "samaritan/index.html", footer_context)


@login_required
def get_all_active_members(request):
    if request.is_ajax:
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')
    data = serializers.serialize("json", members)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_church_roles(request):
    if request.is_ajax:
        roles = ChurchRole.objects.all()
    data = serializers.serialize("json", roles)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_all_addresses(request):
    if request.is_ajax:
        addresses = Address.objects.all()
    data = serializers.serialize("json", addresses)
    return HttpResponse(data, content_type='application/json')


@login_required
def add_new_members(request):
    if request.method == 'POST':
        form = AddMemberForm(request.POST)
        form.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')
