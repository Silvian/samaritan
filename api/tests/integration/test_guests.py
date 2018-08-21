"""API integration guests tests."""

from django.test import TestCase
from api.tests.integration import UserFactory


class TestGuestsIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory(is_superuser=True)

    def test_guests_get_all_active(self):
        self.client.force_login(user=self.user)

        response = self.client.get("/api/guests/getActive")

        self.assertEqual(
            response.status_code,
            200
        )
