"""API integration address tests."""

from django.test import TestCase
from api.tests.integration import UserFactory, AddressFactory
from samaritan.models import Address


class TestAddressIntegrationTestCase(TestCase):
    """Test address model integration tests."""

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.address = AddressFactory()
        self.admin_user = UserFactory(is_superuser = True) # ?


    def test_listing_addresses(self):
        """Test that an authenticated user can view all addresses."""
        self.client.force_login(user=self.user)
        response = self.client.get("/api/addresses/getAll")

        self.assertEquals(
            response.status_code,
            200,
        )

        response_json = response.json()
        self.assertEqual(self.address.id, response_json[0]['pk'])
        self.assertEqual(self.address.number, response_json[0]['fields']['number'])
        self.assertEqual(self.address.street, response_json[0]['fields']['street'])
        self.assertEqual(self.address.locality, response_json[0]['fields']['locality'])
        self.assertEqual(self.address.city, response_json[0]['fields']['city'])
        self.assertEqual(self.address.post_code, response_json[0]['fields']['post_code'])

    def test_create_address(self):
        """ Test that an authenticated user can create a new address"""

        self.client.force_login(user = self.admin_user)

        newAddress = AddressFactory()

        response = self.client.post(
            '/api/addresses/add',
            {
                "number" : newAddress.number,
                "street" : newAddress.street,
                "locality" : newAddress.locality,
                "city" : newAddress.city,
                "post_code" : newAddress.post_code,
            }
        )

        self.assertEqual(
            response.status_code,
            200,
        )
