"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.conf.urls import url
from axes.decorators import watch_login
from . import views

urlpatterns = [
    url(r'^forgot_password/', views.forgot_password, name='forgot_password'),
    url(r'^change_password/', views.change_password, name='change_password'),
    url(r'^forgot/', views.forgot_view, name='forgot'),
    url(r'^reset/', views.reset_view, name='reset'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^access/', watch_login(views.authenticate_user), name='access'),
    url(
        r'^mfa/(?P<token>\b[0-9A-Fa-f]{8}\b(-\b[0-9A-Fa-f]{4}\b){3}-\b[0-9A-Fa-f]{12}\b)/',
        watch_login(views.login_mfa_view), name='mfa'
    ),
]
