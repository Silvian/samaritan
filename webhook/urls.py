"""Webhook URLs"""

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^create/member', views.create_member_webhook, name='createMemberWebhook'),
]
