"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from api.views import success_response, failure_response
from emailservice.forms import EmailOutboxForm
from samaritan.models import Member, ChurchGroup
from django.shortcuts import get_object_or_404

from emailservice.tasks import send_email_task


def send_emails(request, members):
    form = EmailOutboxForm(request.POST or None)
    if form.is_valid():
        outbox = form.save()
        attachment = request.FILES.get(['attachment'][0], default=None)
        if attachment:
            outbox.attachment = attachment
            outbox.save()

        for member in members:
            if member.email:
                send_email_task.delay(
                    outbox_id=outbox.id, member_id=member.id
                )
        return HttpResponse(json.dumps(success_response), content_type='application/json')

    return HttpResponse(json.dumps(failure_response), content_type='application/json')


@login_required
def send_members_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')

        return send_emails(request, members)


@login_required
def send_guests_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=False
        ).order_by('last_name')

        return send_emails(request, members)


@login_required
def send_everyone_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True
        ).order_by('last_name')

        return send_emails(request, members)


@login_required
def send_group_mail(request):
    if request.method == 'POST':
        church_group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        group_members = church_group.members.filter(
            is_active=True
        ).order_by('last_name')

        return send_emails(request, group_members)
