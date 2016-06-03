"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^members/add', views.add_new_members, name='addMember'),
    url(r'^members/update', views.update_member, name='updateMember'),
    url(r'^members/terminate', views.terminate_member, name='terminateMember'),
    url(r'^members/getActive', views.get_all_active_members, name='getActiveMembers'),
    url('^members/getMember', views.get_member, name='getMember'),
    url('^guests/getActive', views.get_all_active_guests, name='getActiveGuests'),
    url('^everyone/getActive', views.get_all_active, name='getEveryoneActive'),
    url('^history/getRecords', views.get_historical_records, name='getHistoryRecords'),
    url('^membership/getTypes', views.get_membership_types, name='getMembershipTypes'),
    url('^membership/getSingle', views.get_membership_type, name='getMembershipSingle'),
    url(r'^roles/getAll', views.get_church_roles, name='getAllRoles'),
    url(r'^roles/getSingle', views.get_role, name='getSingleRoles'),
    url(r'^addresses/add', views.add_new_address, name='addAddress'),
    url(r'^addresses/update', views.update_address, name='updateAddress'),
    url(r'^addresses/getAddress', views.get_address, name='getAddress'),
    url(r'^addresses/getAll', views.get_all_addresses, name='addresses'),
]