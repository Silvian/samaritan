"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib.auth.decorators import login_required

from emailservice.utilities import send_mail_utility

from samaritan.models import Member, ChurchGroup
from django.shortcuts import get_object_or_404


@login_required
def send_members_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')

        return send_mail_utility(request, members)


@login_required
def send_guests_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True, is_member=False
        ).order_by('last_name')

        return send_mail_utility(request, members)


@login_required
def send_everyone_mail(request):
    if request.method == 'POST':
        members = Member.objects.filter(
            is_active=True
        ).order_by('last_name')

        return send_mail_utility(request, members)


@login_required
def send_group_mail(request):
    if request.method == 'POST':
        church_group = get_object_or_404(ChurchGroup, id=request.POST['id'])
        group_members = church_group.members.order_by('last_name').filter(is_active=True)

        return send_mail_utility(request, group_members)
