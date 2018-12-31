"""Tests for emailservice module"""

import mock
from django.test import TestCase
from api.tests.integration import UserFactory, GroupFactory, MemberFactory
from emailservice import tasks


class TestEmailTaskTestCase(TestCase):
    """ Test the email service task test case. """
    @classmethod
    def setUpTestData(cls):
        cls.member = MemberFactory()

    @mock.patch("emailservice.mail.send_email")
    def test_send_email_task(self, send_email_mock):
        """Test send mail task"""
        subject = "Test subject"
        message = "Test message"
        tasks.send_email_task(
            subject=subject, 
            message=message,
            member_first_name=self.member.first_name,
            member_last_name=self.member.last_name,
            member_email=self.member.email,
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
        send_email_task_mock.assert_called_once_with(
            subject=self.subject,
            message=self.message,
            member_first_name=member.first_name,
            member_last_name=member.last_name,
            member_email=member.email,
        )

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
        send_email_task_mock.assert_called_once_with(
            subject=self.subject,
            message=self.message,
            member_first_name=member.first_name,
            member_last_name=member.last_name,
            member_email=member.email,
        )

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
        send_email_task_mock.assert_called_once_with(
            subject=self.subject,
            message=self.message,
            member_first_name=member.first_name,
            member_last_name=member.last_name,
            member_email=member.email,
        )

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
        send_email_task_mock.assert_called_once_with(
            subject=self.subject,
            message=self.message,
            member_first_name=member.first_name,
            member_last_name=member.last_name,
            member_email=member.email,
        )
    
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
