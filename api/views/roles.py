"""
This is the main roles file for Samaritan CMA app

@author: Silvian Dragan
@Date: 06/12/2017
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""
import json

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from api.views import success_response
from samaritan.forms import RoleForm
from samaritan.models import ChurchRole, Member


@login_required
def get_church_roles(request):
    if request.is_ajax:
        roles = ChurchRole.objects.all()
        data = serializers.serialize("json", roles)
        return HttpResponse(data, content_type='application/json')


@login_required
def get_role(request):
    if request.is_ajax:
        role = ChurchRole.objects.get(pk=request.GET['id'])
        data = serializers.serialize("json", [role])
        return HttpResponse(data, content_type='application/json')


@login_required
@staff_member_required
def add_church_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        form.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
@staff_member_required
def update_church_role(request):
    if request.method == 'POST':
        role = get_object_or_404(ChurchRole, id=request.POST['id'])
        form = RoleForm(request.POST or None, instance=role)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
@staff_member_required
def delete_church_role(request):
    if request.method == 'POST':
        church_role = ChurchRole.objects.get(pk=request.POST['id'])

        if not Member.objects.filter(church_role=church_role):
            church_role.delete()
            return HttpResponse(json.dumps(success_response), content_type='application/json')

        else:
            return HttpResponse(json.dumps({
                            'error': "Cannot delete because this role is assigned to a member"}),
                                content_type='application/json')


@login_required
def get_role_members(request):
    if request.is_ajax:
        church_role = get_object_or_404(ChurchRole, pk=request.GET['id'])
        role_members = Member.objects.filter(church_role=church_role, is_active=True)
        data = serializers.serialize("json", role_members)
        return HttpResponse(data, content_type='application/json')
