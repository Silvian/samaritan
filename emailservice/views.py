"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from mail import send_email
from samaritan.models import Member, ChurchGroup
from django.shortcuts import get_object_or_404
import json

success_response = {'success': True}


@login_required
def send_members_group_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')

        for member in members:
            if member.email is not None and member.email != "":
                if not send_email(request.user.email, request.user.first_name, member.first_name,
                                  member.email, request.POST['subject'], request.POST['message']):
                    return HttpResponse(json.dumps({'error': "Cannot send email"}), content_type='application/json')

        return HttpResponse(json.dumps(success_response), content_type='application/json')


@login_required
def send_group_mail(request):
    if request.method == 'POST':
        church_group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        group_members = church_group.members.order_by('last_name')

        for member in group_members:
            if member.email is not None and member.email != "":
                if not send_email(request.user.email, request.user.first_name, member.first_name,
                                  member.email, request.POST['subject'], request.POST['message']):
                    return HttpResponse(json.dumps({'error': "Cannot send email"}), content_type='application/json')

        return HttpResponse(json.dumps(success_response), content_type='application/json')
