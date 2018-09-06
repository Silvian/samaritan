"""Message service views."""

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from .models import SMSMessageConfiguration
from .tasks import send_sms_task
from samaritan.models import ChurchGroup


@login_required
def send_group_message(request):
    if request.method == 'POST':
        church_group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        group_members = church_group.members.order_by('last_name').filter(is_active=True)
        for member in group_members:
            send_sms_task.delay(
                message=request.POST['message'],
                phone=member.telephone,
            )
        return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@login_required
def get_quota(request):
    if request.is_ajax:
        quota_remaining = SMSMessageConfiguration.load().quota_remaining
        return HttpResponse(json.dumps({'result': quota_remaining}), content_type='application/json')
