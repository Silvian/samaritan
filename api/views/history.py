"""
This is the main history file for Samaritan CMA app

@author: Silvian Dragan
@Date: 06/12/2017
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse

from samaritan.models import Member


@login_required
def get_historical_records(request):
    if request.is_ajax:
        historical = Member.objects.filter(
            is_active=False
        ).order_by('last_name')
        data = serializers.serialize("json", historical)
        return HttpResponse(data, content_type='application/json')
