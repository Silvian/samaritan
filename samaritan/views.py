"""
This is the main views file for Samaritan CMA app

@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Please note: All methods and classes in here must be secure (i.e. use @login_required decorators)
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from constants import SettingsConstants


class IndexView(LoginRequiredMixin, TemplateView):
    """Index view."""

    template_name = "samaritan/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        return context


class MembersView(LoginRequiredMixin, TemplateView):
    """Members view."""

    template_name = "samaritan/members.html"

    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'members'
        return context


class GuestsView(LoginRequiredMixin, TemplateView):
    """Guests view."""

    template_name = "samaritan/guests.html"

    def get_context_data(self, **kwargs):
        context = super(GuestsView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'guests'
        return context


class EveryoneView(LoginRequiredMixin, TemplateView):
    """Everyone view."""

    template_name = "samaritan/everyone.html"

    def get_context_data(self, **kwargs):
        context = super(EveryoneView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'everyone'
        return context


class GroupsView(LoginRequiredMixin, TemplateView):
    """Groups view."""

    template_name = "samaritan/groups.html"

    def get_context_data(self, **kwargs):
        context = super(GroupsView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'groups'
        return context


class RolesView(LoginRequiredMixin, TemplateView):
    """Roles view."""

    template_name = "samaritan/roles.html"

    def get_context_data(self, **kwargs):
        context = super(RolesView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'roles'
        return context


class HistoricalView(LoginRequiredMixin, TemplateView):
    """Historical view."""

    template_name = "samaritan/history.html"

    def get_context_data(self, **kwargs):
        context = super(HistoricalView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'history'
        return context


class RoleMembersView(LoginRequiredMixin, TemplateView):
    """Role members view."""

    template_name = "samaritan/views/role_members_view.html"

    def get_context_data(self, **kwargs):
        context = super(RoleMembersView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'roles'
        return context


class GroupMembersView(LoginRequiredMixin, TemplateView):
    """Group members view."""

    template_name = "samaritan/views/group_members_view.html"

    def get_context_data(self, **kwargs):
        context = super(GroupMembersView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'groups'
        return context


class GroupMembersAddView(LoginRequiredMixin, TemplateView):
    """Group members add view."""

    template_name = "samaritan/views/group_members_add.html"

    def get_context_data(self, **kwargs):
        context = super(GroupMembersAddView, self).get_context_data(**kwargs)
        footer_context = SettingsConstants.get_settings()
        context.update(footer_context)
        context['activate'] = 'groups'
        return context
