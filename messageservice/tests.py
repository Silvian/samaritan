"""Message service tests."""

import mock
from django.test import TestCase

from factory.django import DjangoModelFactory

from messageservice import tasks
from api.tests.integration import UserFactory, GroupFactory, MemberFactory
from messageservice.models import SMSMessageConfiguration


class SMSMessageConfigurationFactory(DjangoModelFactory):
    """Factory for SMS Message Configuration."""

    send_message = True

    class Meta:
        model = SMSMessageConfiguration


class TestSMSMessageTaskTestCase(TestCase):
    """Test the sms message task test case."""
    @classmethod
    def setUpTestData(cls):
        cls.member = MemberFactory()
        cls.sms_config = SMSMessageConfigurationFactory()

    @mock.patch("messageservice.service.SMSService.send_sms")
    def test_send_sms_message_task(self, send_sms_mock):
        """Test send sms message task"""
        send_sms_mock.return_value = {
            'success': True,
        }
        message = "Hello World"
        self.member.telephone = "+441234567890"
        self.member.save()

        tasks.send_sms_task(message=message, phone=self.member.telephone)

        send_sms_mock.assert_called_once_with(
            message,
            self.member.telephone
        )


class TestMessageIntegrationTestCase(TestCase):
    """Test the message integration."""

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_superuser=True)
        cls.member = MemberFactory(is_active=True)
        cls.group = GroupFactory(members=[cls.member])

    @mock.patch("messageservice.tasks.send_sms_task.delay")
    def test_send_group_message(self, send_sms_task_mock):
        """Test send group message."""
        self.client.force_login(user=self.user)
        message = "Hello World"

        response = self.client.post(
            '/message/send/group',
            {
                "id": self.group.id,
                "message": message,
            }
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        send_sms_task_mock.assert_called_once_with(
            message=message,
            phone=str(self.member.telephone),
        )

    def test_not_authenticated_send_group_message(self):
        """Test that a non-authenticated user cannot send group message."""
        response = self.client.post(
            '/message/send/group',
            {
                "id": self.group.id,
                "message": "Hello",
            }
        )

        self.assertEqual(
            response.status_code,
            302,
        )
