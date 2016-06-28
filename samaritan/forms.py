"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main forms file to describe web page forms based on models for the Samaritan CMA app.
"""

from django import forms
from models import Member, Address, ChurchRole, ChurchGroup


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'date_of_birth', 'telephone', 'email', 'address',
                  'details', 'is_baptised', 'baptismal_date', 'baptismal_place', 'is_member',
                  'membership_type', 'membership_date', 'church_role', 'is_active')


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Address
        fields = ('number', 'street', 'locality', 'city', 'post_code')


class RoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ChurchRole
        fields = ('name', 'description')


class GroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ChurchGroup
        fields = ('name', 'description', 'members')
