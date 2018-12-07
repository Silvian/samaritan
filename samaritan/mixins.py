"""
@author: Silvian Dragan
@Date: 27/11/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Custom mixins file.
"""
from django.contrib.auth.mixins import AccessMixin


class StaffRoleRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()

        return super(StaffRoleRequiredMixin, self).dispatch(
                request, *args, **kwargs)
