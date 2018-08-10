"""API integration history tests."""

from django.test import TestCase
from api.tests.integration import UserFactory


class TestEveryoneIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)

    def test_list_historical_records(self):
        """Test that an authenticated user can list historical records."""
        self.client.force_login(user=self.user)
        response = self.client.get("/api/history/getRecords")

        self.assertEqual(
            response.status_code,
            200
        )

    def test_not_authenticated_list_historical_records(self):
        """Test that a not authenticated user cannot list everyone active."""
        response = self.client.get("/api/history/getRecords")

        self.assertEqual(
            response.status_code,
            302
        )
