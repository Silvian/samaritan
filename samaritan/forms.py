"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main forms file to describe web page forms based on models for the Samaritan CMA app.
"""

from django import forms
from models import Member


class AddMemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddMemberForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'date_of_birth', 'telephone', 'email', 'address',
                  'is_baptised', 'baptismal_date', 'is_member', 'church_role', 'is_active')
