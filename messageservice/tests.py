# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest.mock import patch
from django.test import TestCase

import factory

from messageservice import tasks
from samaritan.models import Member
from api.tests.integration import UserFactory, GroupFactory

# Create your tests here.


class TestSMSMessageTaskTestCase(TestCase):
    """Test the sms message task test case."""
    @classmethod
    def setUpTestData(cls):
        cls.sms_message = factory.Faker('text')
        cls.user = UserFactory(is_superuser=True)
        cls.group = GroupFactory()

    @patch("messageservice.service.SMSService.send_sms")
    def test_send_sms_message_task(self, send_sms_mock):
        """Test send sms message task"""
        member = Member.objects.get(user=self.user)
        member.telephone = "+441234567890"
        member.save()

        tasks.send_sms_task(message=self.sms_message, mobile=member.telephone)

        send_sms_mock.assert_called_once_with(
            message=self.sms_message,
            mobile=member.telephone
        )