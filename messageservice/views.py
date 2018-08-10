# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse

from .tasks import send_sms_task
from samaritan.models import Member, ChurchGroup

# Create your views here.
@login_required
def send_group_message(request):
    if request.method == 'POST':
        church_group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        group_members = church_group.members.order_by('last_name').filter(is_active=True)
        for member in group_members:
            send_sms_task.delay(
                phone=request.POST['mobile'],
                message=request.POST['message']
            )
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
