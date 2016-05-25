"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from writer import write_to_excel, file_name_date
from samaritan.models import Member


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
