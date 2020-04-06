"""
@author: Silvian Dragan
@Date: 06/4/2020
@Copyright: Copyright 2020, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django import forms

from models import EmailOutbox


class EmailOutboxForm(forms.ModelForm):
    """EmailOutbox model form."""

    def __init__(self, *args, **kwargs):
        super(EmailOutboxForm, self).__init__(*args, **kwargs)

    class Meta:
        model = EmailOutbox
        fields = ('subject', 'message')
