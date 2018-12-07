"""Authentication forms."""

from django import forms
from django_common.auth_backends import User


class UserForm(forms.ModelForm):
    """User model form."""

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        required_fields = ('username', 'email',)


class UserDetailsForm(forms.ModelForm):
    """User details model form."""

    def __init__(self, *args, **kwargs):
        super(UserDetailsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
        )
        required_fields = (
            'username',
            'email',
            'is_staff',
        )
