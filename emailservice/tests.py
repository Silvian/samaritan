"""Tests for emailservice module"""

import mock
from django.test import TestCase

from factory.django import DjangoModelFactory

from api.tests.integration import UserFactory, GroupFactory, MemberFactory
from emailservice import tasks
from emailservice.models import EmailOutbox


class EmailOutboxFactory(DjangoModelFactory):
    """Factory for Email Outbox model."""

    subject = "Test subject"
    message = "Test message"

    class Meta:
        model = EmailOutbox


class TestEmailTaskTestCase(TestCase):
    """ Test the email service task test case. """
    @classmethod
    def setUpTestData(cls):
        cls.member = MemberFactory()
        cls.outbox = EmailOutboxFactory()

    @mock.patch("emailservice.mail.send_email")
    def test_send_email_task(self, send_email_mock):
        """Test send mail task"""
        tasks.send_email_task(
            outbox_id=self.outbox.id,
            member_id=self.member.id,
        )
        self.assertTrue(send_email_mock)


class EmailServiceTestIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.group = GroupFactory()
        self.subject = "Testing subject"
        self.message = "Testing message"

    @mock.patch("emailservice.tasks.send_email_task.delay")
    def test_send_members_mail(self, send_email_task_mock):
        """Test that an authenticated user can send emails to all members"""
        self.client.force_login(user=self.user)
        member = MemberFactory(is_active=True, is_member=True)
        response = self.client.post(
            "/email/send/members",
            {
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
        outbox = EmailOutbox.objects.all().last()
        self.assertIsNotNone(outbox)
        send_email_task_mock.assert_called_once_with(
            outbox_id=outbox.id, member_id=member.id,
        )
        response_json = response.json()
        self.assertTrue(response_json["success"])

    @mock.patch("emailservice.tasks.send_email_task.delay")
    def test_send_guests_mail(self, send_email_task_mock):
        """Test that an authenticated user can send emails to all guests"""
        self.client.force_login(user=self.user)
        member = MemberFactory(is_active=True, is_member=False)
        response = self.client.post(
            "/email/send/guests",
            {
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
        outbox = EmailOutbox.objects.all().last()
        self.assertIsNotNone(outbox)
        send_email_task_mock.assert_called_once_with(
            outbox_id=outbox.id, member_id=member.id,
        )
        response_json = response.json()
        self.assertTrue(response_json["success"])

    @mock.patch("emailservice.tasks.send_email_task.delay")
    def test_send_everyone_mail(self, send_email_task_mock):
        """Test that an authenticated user can send emails to everyone"""
        self.client.force_login(user=self.user)
        member = MemberFactory(is_active=True)
        response = self.client.post(
            "/email/send/everyone",
            {
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
        outbox = EmailOutbox.objects.all().last()
        self.assertIsNotNone(outbox)
        send_email_task_mock.assert_called_once_with(
            outbox_id=outbox.id, member_id=member.id,
        )
        response_json = response.json()
        self.assertTrue(response_json["success"])

    @mock.patch("emailservice.tasks.send_email_task.delay")
    def test_send_group_mail(self, send_email_task_mock):
        """Test that an authenticated user can send emails to a group"""
        self.client.force_login(user=self.user)
        member = MemberFactory(is_active=True)
        self.group.members.add(member)
        response = self.client.post(
            "/email/send/group",
            {
                "id": self.group.id,
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
        outbox = EmailOutbox.objects.all().last()
        self.assertIsNotNone(outbox)
        send_email_task_mock.assert_called_once_with(
            outbox_id=outbox.id, member_id=member.id,
        )
        response_json = response.json()
        self.assertTrue(response_json["success"])
    
    def test_not_authenticated_send_members_mail(self):
        """Test that a non-authenticated user cannot send emails to all members"""
        response = self.client.post(
            "/email/send/members",
            {
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_send_guests_mail(self):
        """Test that a non-authenticated user cannot send emails to all guests"""
        response = self.client.post(
            "/email/send/guests",
            {
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_send_everyone_mail(self):
        """Test that a non-authenticated user cannot send emails to everyone"""
        response = self.client.post(
            "/email/send/everyone",
            {
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_send_group_mail(self):
        """Test that a non-authenticated user cannot send emails to a group"""
        response = self.client.post(
            "/email/send/group",
            {
                "id": self.group.id,
                "subject": self.subject,
                "message": self.message,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
