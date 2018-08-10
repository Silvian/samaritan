"""API integration everyone tests."""

from django.test import TestCase
from api.tests.integration import UserFactory


class TestEveryoneIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)

    def test_list_everyone_active(self):
        """Test that an authenticated user can list everyone."""
        self.client.force_login(user=self.user)
        response = self.client.get("/api/everyone/getActive")

        self.assertEqual(
            response.status_code,
            200
        )

    def test_not_authenticated_list_everyone_active(self):
        """Test that a not authenticated user cannot list everyone active."""
        response = self.client.get("/api/everyone/getActive")

        self.assertEqual(
            response.status_code,
            302
        )
