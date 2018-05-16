"""samaritan URL Configuration

@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls', namespace="api")),
    url(r'^authenticate/', include('authentication.urls', namespace="authenticate")),
    url(r'^export/', include('export.urls', namespace="export")),
    url(r'^email/', include('emailservice.urls', namespace="email")),
    url(r'^members/', views.MembersView.as_view(), name='members'),
    url(r'^guests/', views.GuestsView.as_view(), name='guests'),
    url(r'^everyone/', views.EveryoneView.as_view(), name='everyone'),
    url(r'^groups/', views.GroupsView.as_view(), name='groups'),
    url(r'^roles/', views.RolesView.as_view(), name='roles'),
    url(r'^history/', views.HistoricalView.as_view(), name='history'),
    url(r'^user/', views.UserProfileView.as_view(), name='user'),
    url(r'^views/role_members', views.RoleMembersView.as_view(), name='roleMembers'),
    url(r'^views/group_members', views.GroupMembersView.as_view(), name='groupMembers'),
    url(r'^views/group_add', views.GroupMembersAddView.as_view(), name='addGroupMembers'),
    url(r'^$', views.IndexView.as_view(), name='index'),
]
