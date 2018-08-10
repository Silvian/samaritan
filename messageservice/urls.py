from django.conf.urls import url
import views

urlpatterns = [
    url(r'^send/group', views.send_group_message, name='sendGroupMessage'),
]
