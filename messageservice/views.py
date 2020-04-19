"""Message service views."""

import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from api.views import success_response
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
        return HttpResponse(json.dumps(success_response), content_type='application/json')
