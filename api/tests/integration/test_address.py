"""API integration address tests."""

from django.test import TestCase
from api.tests.integration import UserFactory, AddressFactory


class TestAddressIntegrationTestCase(TestCase):
    """Test address model integration tests."""

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.address = AddressFactory()

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
        """ Test that an authenticated user can create a new address."""
        self.client.force_login(user=self.admin_user)
        new_address = AddressFactory()

        response = self.client.post(
            '/api/addresses/add',
            {
                "number": new_address.number,
                "street": new_address.street,
                "locality": new_address.locality,
                "city": new_address.city,
                "post_code": new_address.post_code,
            }
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_delete_address(self):
        """Test that an authenticated user can delete an existing address."""
        self.client.force_login(user=self.user)
        response = self.client.get("/api/addresses/getAll")

        self.assertEquals(
            response.status_code,
            200,
        )
        response_json = response.json()
        del response_json[0]

        self.assertEquals(len(response_json), 0)

    def test_update_address(self):
        """Test that an authenticated user can update an existing address."""
        self.client.force_login(user=self.admin_user)
        new_address = AddressFactory()
        response = self.client.post(
            "/api/addresses/update/",
            {
                "id": self.address.id,
                "number": new_address.number,
                "city": new_address.city,
                "locality": new_address.locality,
                "post_code": new_address.post_code,
                "street": new_address.street,
            }
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_user_power_list_addresses(self):
        """Test that a not authenticated user cannot do list addresses."""
        response = self.client.get("/api/addresses/getAll")

        self.assertEqual(
            response.status_code,
            302
        )

    def test_user_power_get_address(self):
        """Test that a not authenticated user cannot list an address."""
        response = self.client.get("/api/addresses/getAddress")

        self.assertEqual(
            response.status_code,
            302
        )

    def test_user_power_create_address(self):
        """Test that a not authenticated user create an address."""
        new_address = AddressFactory()
        response = self.client.post(
            "/api/addresses/add",
            {
                "number": new_address.number,
                "street": new_address.street,
                "locality": new_address.locality,
                "city": new_address.city,
                "post_code": new_address.post_code,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_user_power_update_address(self):
        """Test that a not authenticated user cannot update an address."""
        new_address = AddressFactory()
        response = self.client.post(
            "/api/addresses/update/",
            {
                "id": self.address.id,
                "number": new_address.number,
                "city": new_address.city,
                "locality": new_address.locality,
                "post_code": new_address.post_code,
                "street": new_address.street,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )


