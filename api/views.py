"""
This is the main views file for Samaritan CMA app

@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""

from django.http import HttpResponse
from django.core import serializers
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from samaritan.models import Member, ChurchRole, Address, MembershipType
from samaritan.forms import MemberForm, AddressForm, RoleForm
from django.shortcuts import get_object_or_404
import json

success_response = {'success': True}


@login_required
def get_all_active(request):
    if request.is_ajax:
        everyone = Member.objects.filter(
            is_active=True
        ).order_by('last_name')
    data = serializers.serialize("json", everyone)
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
def get_all_active_guests(request):
    if request.is_ajax:
        guests = Member.objects.filter(
            is_active=True, is_member=False
        ).order_by('last_name')
    data = serializers.serialize("json", guests)
    return HttpResponse(data, content_type='application/json')


@login_required
def get_historical_records(request):
    if request.is_ajax:
        historical = Member.objects.filter(
            is_active=False
        ).order_by('last_name')
    data = serializers.serialize("json", historical)
    return HttpResponse(data, content_type='application/json')


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
def add_church_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        form.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def update_church_role(request):
    if request.method == 'POST':
        role = get_object_or_404(ChurchRole, id=request.POST['id'])
        form = RoleForm(request.POST or None, instance=role)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
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


@login_required
def get_membership_types(request):
    if request.is_ajax:
        membership_types = MembershipType.objects.all()

    data = serializers.serialize("json", membership_types)
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
        form = MemberForm(request.POST)
        form.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def add_new_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        new_address = form.save()
        return HttpResponse(json.dumps({'address': new_address.pk}), content_type='application/json')


@login_required
def get_member(request):
    if request.is_ajax:
        member = Member.objects.get(pk=request.GET['id'])
    data = serializers.serialize("json", [member])
    return HttpResponse(data, content_type='application/json')


@login_required
def get_address(request):
    if request.is_ajax:
        address = Address.objects.get(pk=request.GET['id'])
    data = serializers.serialize("json", [address])
    return HttpResponse(data, content_type='application/json')


@login_required
def get_membership_type(request):
    if request.is_ajax:
        membership_type = MembershipType.objects.get(pk=request.GET['id'])
    data = serializers.serialize("json", [membership_type])
    return HttpResponse(data, content_type='application/json')


@login_required
def update_member(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=request.POST['id'])
        form = MemberForm(request.POST or None, instance=member)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def update_address(request):
    if request.method == 'POST':
        address = get_object_or_404(Address, id=request.POST['id'])
        form = AddressForm(request.POST or None, instance=address)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def terminate_member(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=request.POST['id'])
        member.is_active = False
        member.notes = request.POST['notes']
        member.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def reinstate_member(request):
    if request.method == 'POST':
        member = get_object_or_404(Member, id=request.POST['id'])
        member.is_active = True
        member.save()
        return HttpResponse(json.dumps(success_response), content_type='application/json')
