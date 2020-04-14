"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.conf.urls import url
from views import (
    accounts,
    address,
    members,
    guests,
    everyone,
    history,
    roles,
    groups,
    profile,
)


urlpatterns = [
    url(r'^members/add', members.add_new_members, name='addMember'),
    url(r'^members/update', members.update_member, name='updateMember'),
    url(r'^members/delete', members.delete_member, name='deleteMember'),
    url(r'^members/terminate', members.terminate_member, name='terminateMember'),
    url(r'^members/reinstate', members.reinstate_member, name='reinstateMember'),
    url(r'^members/getActive', members.get_all_active_members, name='getActiveMembers'),
    url(r'^members/getMember', members.get_member, name='getMember'),
    url(r'^guests/getActive', guests.get_all_active_guests, name='getActiveGuests'),
    url(r'^everyone/getActive', everyone.get_all_active, name='getEveryoneActive'),
    url(r'^history/getRecords', history.get_historical_records, name='getHistoryRecords'),
    url(r'^membership/getTypes', members.get_membership_types, name='getMembershipTypes'),
    url(r'^membership/getSingle', members.get_membership_type, name='getMembershipSingle'),
    url(r'^roles/getAll', roles.get_church_roles, name='getAllRoles'),
    url(r'^roles/getSingle', roles.get_role, name='getSingleRoles'),
    url(r'^roles/add', roles.add_church_role, name='addRole'),
    url(r'^roles/update', roles.update_church_role, name='updateRole'),
    url(r'^roles/delete', roles.delete_church_role, name='deleteRole'),
    url(r'^roles/getMembers', roles.get_role_members, name='getRoleMembers'),
    url(r'^addresses/add', address.add_new_address, name='addAddress'),
    url(r'^addresses/update', address.update_address, name='updateAddress'),
    url(r'^addresses/getAddress', address.get_address, name='getAddress'),
    url(r'^addresses/getAll', address.get_all_addresses, name='addresses'),
    url(r'^addresses/delete', address.delete_address, name='deleteAddress'),
    url(r'^groups/getAll', groups.get_all_groups, name='getAllGroups'),
    url(r'^groups/getSingle', groups.get_group, name='getGroup'),
    url(r'^groups/add', groups.add_new_group, name='addGroup'),
    url(r'^groups/update', groups.update_group, name='updateGroup'),
    url(r'^groups/delete', groups.delete_group, name='deleteGroup'),
    url(r'^groups/getMembers', groups.get_group_members, name='getGroupMembers'),
    url(r'^groups/membersToAdd', groups.get_members_to_add, name='getGroupMembersToAdd'),
    url(r'^groups/memberAdd', groups.add_group_member, name='addGroupMembers'),
    url(r'^groups/memberDelete', groups.delete_group_member, name='deleteGroupMember'),
    url(r'^profile/get', profile.get_user_profile, name='getUserProfile'),
    url(r'^profile/update', profile.update_user_profile, name='updateUserProfile'),
    url(r'profile/sendCode', profile.send_mfa_code, name='sendMFACode'),
    url(r'profile/verifyCode', profile.verify_mfa_code, name='verifyMFACode'),
    url(r'profile/disableMFA', profile.disable_mfa, name='disableMFA'),
    url(r'^accounts/getAll', accounts.get_all_users, name='getAllUserAccounts'),
    url(r'^accounts/getSingle', accounts.get_user_details, name='getUserAccount'),
    url(r'^accounts/add', accounts.create_new_user, name="addUserAccount"),
    url(r'^accounts/activate', accounts.activate_user, name="activateUserAccount"),
    url(r'^accounts/resendEmail', accounts.resend_welcome_email, name="resendEmailUserAccount"),
    url(r'^accounts/update', accounts.update_user, name="updateUserAccount"),
    url(r'^accounts/delete', accounts.delete_user, name="deleteUserAccount"),
]
