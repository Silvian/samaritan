"""Tests for export module"""

from django.test import TestCase
from api.tests.integration import UserFactory, RoleFactory



class ExportTestIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.role = RoleFactory()

    def test_download_members(self):
        """Test that an authenticated user can download a list of members"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/export/download/members/excel"
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_download_guests(self):
        """Test that an authenticated user can download a list of guests"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/export/download/guests/excel"
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_download_historical(self):
        """Test that an authenticated user can download all historical records"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/export/download/historical/excel"
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_download_everyone(self):
        """Test that an authenticated user can download a full list"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/export/download/everyone/excel"
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_download_role_members(self):
        """Test that an authenticated user can download a list of roles"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/export/download/role/excel",
            {
                "id": self.role.id,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_not_authenticated_download_members(self):
        """Test that a non-authenticated user cannot download a list of members"""
        response = self.client.get(
            "/export/download/members/excel"
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_download_guests(self):
        """Test that a non-authenticated user cannot download a list of guests"""
        response = self.client.get(
            "/export/download/guests/excel"
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_download_historical(self):
        """Test that a non-authenticated user cannot download a list of historical records"""
        response = self.client.get(
            "/export/download/historical/excel"
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_download_everyone(self):
        """Test that a non-authenticated user cannot download a full list"""
        response = self.client.get(
            "/export/download/everyone/excel"
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_download_role_members(self):
        """Test that a non-authenticated user cannot download a list of roles"""
        response = self.client.get(
            "/export/download/role/excel",
            {
                "id": self.role.id,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
