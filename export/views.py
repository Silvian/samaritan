"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from writer import write_to_excel, file_name_date
from samaritan.models import Member, ChurchRole


@login_required
def download_members(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=MembersList-'+file_name_date()+'.xlsx'
        members = Member.objects.filter(
            is_active=True, is_member=True
        ).order_by('last_name')
        data = list(members)
        download_data = write_to_excel(data, "Members")
        response.write(download_data)
        return response


@login_required
def download_guests(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=GuestsList-'+file_name_date()+'.xlsx'
        members = Member.objects.filter(
            is_active=True, is_member=False
        ).order_by('last_name')
        data = list(members)
        download_data = write_to_excel(data, "Guests")
        response.write(download_data)
        return response


@login_required
def download_everyone(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=FullList-'+file_name_date()+'.xlsx'
        members = Member.objects.filter(
            is_active=True
        ).order_by('last_name')
        data = list(members)
        download_data = write_to_excel(data, "Full")
        response.write(download_data)
        return response


@login_required
def download_historical(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=HistoricalRecordsList-'+file_name_date()+'.xlsx'
        members = Member.objects.filter(
            is_active=False
        ).order_by('last_name')
        data = list(members)
        download_data = write_to_excel(data, "Historical Records")
        response.write(download_data)
        return response


@login_required
def download_role_members(request):
    if request.method == 'GET':
        church_role = get_object_or_404(ChurchRole, pk=request.GET['id'])
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = (
            'attachment; filename=RoleList-' + church_role.name + '-' + file_name_date() + '.xlsx')
        role_members = Member.objects.filter(
            church_role=church_role,
            is_active=True
        ).order_by('last_name')
        data = list(role_members)
        download_data = write_to_excel(data, "Role list " + church_role.name)
        response.write(download_data)
        return response
