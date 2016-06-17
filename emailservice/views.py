"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from mail import send_group_emails
from samaritan.models import Member
import json

success_response = {'success': True}


@login_required
def send_group_mail(request):
    if request.method == 'GET':
        if send_group_emails(request.user.email, request.user.username, 'Test email'):
            return HttpResponse(json.dumps(success_response), content_type='application/json')

        else:
            return HttpResponse(json.dumps({'error': "Cannot send email"}), content_type='application/json')
