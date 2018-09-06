"""Message service urls."""

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^send/group', views.send_group_message, name='sendGroupMessage'),
    url(r'^getQuota', views.get_quota, name='getQuota'),
]
