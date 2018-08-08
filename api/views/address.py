"""
This is the main address file for Samaritan CMA app

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
from samaritan.forms import AddressForm
from samaritan.models import Address


@login_required
def get_all_addresses(request):
    if request.is_ajax:
        addresses = Address.objects.all()
        data = serializers.serialize("json", addresses)
        return HttpResponse(data, content_type='application/json')


@login_required
def get_address(request):
    if request.is_ajax:
        address = Address.objects.get(pk=request.GET['id'])
        data = serializers.serialize("json", [address])
        return HttpResponse(data, content_type='application/json')


@login_required
@staff_member_required
def add_new_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        new_address = form.save()
        return HttpResponse(json.dumps({'address': new_address.pk}), content_type='application/json')


@login_required
@staff_member_required
def update_address(request):
    if request.method == 'POST':
        address = get_object_or_404(Address, id=request.POST['id'])
        form = AddressForm(request.POST or None, instance=address)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
@staff_member_required
def delete_address(request):
    if request.method == 'POST':
        address = Address.objects.get(pk=request.POST['id'])
        address.delete()
        return HttpResponse(json.dumps(success_response), content_type='application/json')