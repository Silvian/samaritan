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
    url(r'^members/delete', views.delete_member, name='deleteMember'),
    url(r'^members/terminate', views.terminate_member, name='terminateMember'),
    url(r'^members/reinstate', views.reinstate_member, name='reinstateMember'),
    url(r'^members/getActive', views.get_all_active_members, name='getActiveMembers'),
    url(r'^members/getMember', views.get_member, name='getMember'),
    url(r'^guests/getActive', views.get_all_active_guests, name='getActiveGuests'),
    url(r'^everyone/getActive', views.get_all_active, name='getEveryoneActive'),
    url(r'^history/getRecords', views.get_historical_records, name='getHistoryRecords'),
    url(r'^membership/getTypes', views.get_membership_types, name='getMembershipTypes'),
    url(r'^membership/getSingle', views.get_membership_type, name='getMembershipSingle'),
    url(r'^roles/getAll', views.get_church_roles, name='getAllRoles'),
    url(r'^roles/getSingle', views.get_role, name='getSingleRoles'),
    url(r'^roles/add', views.add_church_role, name='addRole'),
    url(r'^roles/update', views.update_church_role, name='updateRole'),
    url(r'^roles/delete', views.delete_church_role, name='deleteRole'),
    url(r'^roles/getMembers', views.get_role_members, name='getRoleMembers'),
    url(r'^addresses/add', views.add_new_address, name='addAddress'),
    url(r'^addresses/update', views.update_address, name='updateAddress'),
    url(r'^addresses/getAddress', views.get_address, name='getAddress'),
    url(r'^addresses/getAll', views.get_all_addresses, name='addresses'),
    url(r'^groups/getAll', views.get_all_groups, name='getAllGroups'),
    url(r'^groups/getSingle', views.get_group, name='getGroup'),
    url(r'^groups/add', views.add_new_group, name='addGroup'),
    url(r'^groups/update', views.update_group, name='updateGroup'),
    url(r'^groups/delete', views.delete_group, name='deleteGroup'),
    url(r'^groups/getMembers', views.get_group_members, name='getGroupMembers'),
    url(r'^groups/membersToAdd', views.get_members_to_add, name='getGroupMembersToAdd'),
    url(r'^groups/memberAdd', views.add_group_member, name='addGroupMembers'),
    url(r'^groups/memberDelete', views.delete_group_member, name='deleteGroupMember'),
]
