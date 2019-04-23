"""
This is the main members file for Samaritan CMA app

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

from api.views import success_response, failure_response
from samaritan.forms import MemberForm
from samaritan.models import MembershipType, Member


@login_required
def get_membership_types(request):
    if request.is_ajax:
        membership_types = MembershipType.objects.all()
        data = serializers.serialize("json", membership_types)
        return HttpResponse(data, content_type='application/json')


@login_required
def get_membership_type(request):
    if request.is_ajax:
        membership_type = MembershipType.objects.get(pk=request.GET['id'])
        data = serializers.serialize("json", [membership_type])
        return HttpResponse(data, content_type='application/json')


@login_required
def get_all_active_members(request):
    if request.is_ajax:
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')
        data = serializers.serialize("json", members)
        return HttpResponse(data, content_type='application/json')


@login_required
def get_member(request):
    if request.is_ajax:
        member = Member.objects.get(pk=request.GET['id'])
        data = serializers.serialize("json", [member])
        return HttpResponse(data, content_type='application/json')


@login_required
@staff_member_required
def add_new_members(request):
    if request.method == 'POST':
        form = MemberForm(request.POST or None)
        if form.is_valid():
            member = form.save()
            profile_image = request.FILES.get(['profile_pic'][0], default=None)
            if profile_image:
                member.profile_pic = profile_image
                member.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')

        return HttpResponse(json.dumps(failure_response), content_type='application/json')


@login_required
@staff_member_required
def update_member(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=request.POST['id'])
        form = MemberForm(request.POST or None, instance=member)
        if form.is_valid():
            profile_image = request.FILES.get(['profile_pic'][0], default=None)
            if profile_image:
                member.profile_pic = profile_image
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')

        return HttpResponse(json.dumps(failure_response), content_type='application/json')


@login_required
@staff_member_required
def delete_member(request):
    if request.method == 'POST':
        member = Member.objects.get(pk=request.POST['id'])
        member.delete()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
@staff_member_required
def terminate_member(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=request.POST['id'])
        member.is_active = False
        member.notes = request.POST['notes']
        member.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
@staff_member_required
def reinstate_member(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=request.POST['id'])
        member.is_active = True
        member.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')
