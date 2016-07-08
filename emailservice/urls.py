"""
@author: Silvian Dragan
@Date: 17/06/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^send/members', views.send_members_mail, name='sendMembersEmail'),
    url(r'^send/group', views.send_group_mail, name='sendGroupEmail'),
]
