"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^download/members/excel', views.download_members, name='membersExcel'),
    url(r'^download/guests/excel', views.download_guests, name='guestsExcel'),
    url(r'^download/everyone/excel', views.download_everyone, name='everyoneExcel'),
    url(r'^download/role/excel', views.download_role_members, name='roleMembersExcel'),
    url(r'^download/historical/excel', views.download_historical, name='historicalExcel'),
]
