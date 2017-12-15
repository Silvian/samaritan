"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from samaritan.models import Member, ChurchGroup
from django.shortcuts import get_object_or_404

from emailservice.tasks import send_email_task


@login_required
def send_members_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')

        for member in members:
            if member.email:
                send_email_task.delay(
                    from_email=request.user.email,
                    from_name=request.user.first_name,
                    subject=request.POST['subject'],
                    message=request.POST['message'],
                    member_first_name=member.first_name,
                    member_last_name=member.last_name,
                    member_email=member.email,
                )

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@login_required
def send_guests_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=False
        ).order_by('last_name')

        for member in members:
            if member.email:
                send_email_task.delay(
                    from_email=request.user.email,
                    from_name=request.user.first_name,
                    subject=request.POST['subject'],
                    message=request.POST['message'],
                    member_first_name=member.first_name,
                    member_last_name=member.last_name,
                    member_email=member.email,
                )

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@login_required
def send_everyone_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True
        ).order_by('last_name')

        for member in members:
            if member.email:
                send_email_task.delay(
                    from_email=request.user.email,
                    from_name=request.user.first_name,
                    subject=request.POST['subject'],
                    message=request.POST['message'],
                    member_first_name=member.first_name,
                    member_last_name=member.last_name,
                    member_email=member.email,
                )

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@login_required
def send_group_mail(request):
    if request.method == 'POST':
        church_group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        group_members = church_group.members.order_by('last_name').filter(is_active=True)

        for member in group_members:
            if member.email:
                send_email_task.delay(
                    from_email=request.user.email,
                    from_name=request.user.first_name,
                    subject=request.POST['subject'],
                    message=request.POST['message'],
                    member_first_name=member.first_name,
                    member_last_name=member.last_name,
                    member_email=member.email,
                )

        return HttpResponse(json.dumps({'success': True}), content_type='application/json')
