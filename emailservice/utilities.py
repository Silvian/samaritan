"""
Mail utilities.

@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""
import json

from django.http import HttpResponse

from emailservice.mail import send_email


def send_mail_utility(request, members):

    for member in members:
        if member.email is not None and member.email != "":
            if not send_email(request.user.email, request.user.first_name, member.first_name,
                              member.email, request.POST['subject'], request.POST['message']):
                return HttpResponse(json.dumps({'error': "Cannot send email"}), content_type='application/json')

    return HttpResponse(json.dumps({'success': True}), content_type='application/json')
