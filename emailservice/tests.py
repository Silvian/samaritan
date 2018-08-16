"""Tests for emailservice module"""

from django.test import TestCase
from api.tests.integration import UserFactory, GroupFactory


class EmailServiceTestIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.group =  GroupFactory()
        
    def test_send_members_mail(self):
        """Test that an authenticated user can send emails to all members"""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/email/send/members",
            {
                "subject": "Testing subject",
                "message": "Testing message"
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_send_guests_mail(self):
        """Test that an authenticated user can send emails to all guests"""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/email/send/guests",
            {
                "subject": "Testing subject",
                "message": "Testing message"
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_send_everyone_mail(self):
        """Test that an authenticated user can send emails to everyone"""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/email/send/everyone",
            {
                "subject": "Testing subject",
                "message": "Testing message"
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_send_group_mail(self):
        """Test that an authenticated user can send emails to a group"""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/email/send/group",
            {
                "id": self.group.id,
                "subject": "Testing subject",
                "message": "Testing message"
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_not_authenticated_send_members_mail(self):
        """Test that a non-authenticated user cannot send emails to all members"""
        response = self.client.post(
            "/email/send/members",
            {
                "subject": "Testing subject",
                "message": "Testing message"
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
                "subject": "Testing subject",
                "message": "Testing message"
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
                "subject": "Testing subject",
                "message": "Testing message"
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
                "subject": "Testing subject",
                "message": "Testing message"
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    