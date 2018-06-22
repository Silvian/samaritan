"""
This is the main groups file for Samaritan CMA app

@author: Silvian Dragan
@Date: 06/12/2017
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""
import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from api.views import success_response
from samaritan.forms import GroupForm
from samaritan.models import ChurchGroup, Member


@login_required
def get_all_groups(request):
    if request.is_ajax:
        groups = ChurchGroup.objects.all().order_by('name')
        data = serializers.serialize("json", groups)
        return HttpResponse(data, content_type='application/json')


@login_required
def get_group(request):
    if request.is_ajax:
        group = ChurchGroup.objects.get(pk=request.GET['id'])
        data = serializers.serialize("json", [group])
        return HttpResponse(data, content_type='application/json')


@login_required
def add_new_group(request):
    if request.method == 'POST':
        group = GroupForm(request.POST)
        group.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def update_group(request):
    if request.method == 'POST':
        group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        form = GroupForm(request.POST or None, instance=group)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def delete_group(request):
    if request.method == 'POST':
        group = ChurchGroup.objects.get(pk=request.POST['id'])
        group.delete()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def get_group_members(request):
    if request.is_ajax:
        church_group = get_object_or_404(ChurchGroup, id=request.GET['id'])
        group_members = church_group.members.order_by('last_name').filter(is_active=True)
        data = serializers.serialize("json", group_members)
        return HttpResponse(data, content_type='application/json')


@login_required
def get_members_to_add(request):
    if request.is_ajax:
        church_group = get_object_or_404(ChurchGroup, id=request.GET['id'])
        group_members = church_group.members.order_by('last_name')
        church_members = Member.objects.filter(
            is_active=True
        ).order_by('last_name')
        data = []
        for member in church_members:
            if member not in group_members:
                data.append(member)

        data = serializers.serialize("json", data)
        return HttpResponse(data, content_type='application/json')


@login_required
def add_group_member(request):
    if request.method == 'POST':
        group = get_object_or_404(ChurchGroup, id=request.POST['group_id'])
        member = Member.objects.get(pk=request.POST['member_id'])
        group.members.add(member)
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def delete_group_member(request):
    if request.method == 'POST':
        group = get_object_or_404(ChurchGroup, id=request.POST['group_id'])
        member = group.members.get(pk=request.POST['member_id'])
        group.members.remove(member)
        return HttpResponse(json.dumps(success_response), content_type='application/json')
