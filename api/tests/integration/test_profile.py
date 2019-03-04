"""API integration profile tests."""

from django.test import TestCase
from api.tests.integration import UserFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from samaritan.settings import MEDIA_ROOT


class TestProfileIntegrationTesting(TestCase):
    """Test profile api url integration tests"""

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
    
    def test_list_profile(self):
        """Test that an authenticated user can list a profile"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/profile/get"
        )
        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()
        self.assertEqual(response_json["username"], self.user.username)
        self.assertEqual(response_json["first_name"], self.user.first_name)
        self.assertEqual(response_json["last_name"], self.user.last_name)
        self.assertEqual(response_json["email"], self.user.email)
        self.assertEqual(response_json["mobile_number"], self.user.profile.mobile_number)

    def test_update_user_profile(self):
        """Test that an authenticate user can update his profile"""
        self.client.force_login(user=self.user)
        profile_image = SimpleUploadedFile(
            name='guest.png',
            content=open(str(MEDIA_ROOT + '/images/guest.png'), 'rb').read(),
            content_type='image/png'
        )
        response = self.client.post(
                "/api/profile/update",
                {
                    "username": "randomname",
                    "first_name": "firstname",
                    "last_name": "lastname",
                    "email": "sample@email.com",
                    "mobile_number": "+441234566",
                    "profile_image": profile_image,
                }
            )
        self.assertEqual(
            response.status_code,
            200
        )

        response_json = response.json()
        self.assertEqual(response_json["success"], True)
