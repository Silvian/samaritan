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
    url(r'^authenticate/', include('authentication.urls', namespace="authenticate")),
    url(r'^api/members/add', views.add_new_members, name='addMember'),
    url(r'^api/members/update', views.update_member, name='updateMember'),
    url(r'^api/members/getActive', views.get_all_active_members, name='getActiveMembers'),
    url(r'^api/roles/get', views.get_church_roles, name='getRoles'),
    url(r'^api/addresses/add', views.add_new_address, name='addAddress'),
    url(r'^api/addresses/update', views.update_address, name='updateAddress'),
    url(r'^api/addresses/get', views.get_all_addresses, name='addresses'),
    url(r'^$', views.index_view, name='index'),
]
