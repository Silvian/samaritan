"""Api integration accounts tests."""
import mock

from django.test import TestCase
from api.tests.integration import UserFactory


class TestAccountsIntegrationTesting(TestCase):
    """Test accounts api url integration tests."""

    def setUp(self):
        self.super_user = UserFactory(is_superuser=True, is_staff=True)
        self.admin_user = UserFactory(is_staff=True)

    def test_list_user_accounts(self):
        """Test that all user accounts are listed excluding super users."""
        self.client.force_login(user=self.admin_user)
        response = self.client.get(
            "/api/accounts/getAll"
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        # check that super users are not listed
        self.assertEqual(len(response_json), 1)

        self.assertEqual(response_json[0]["fields"]["username"], self.admin_user.username)
        self.assertEqual(response_json[0]["fields"]["first_name"], self.admin_user.first_name)
        self.assertEqual(response_json[0]["fields"]["last_name"], self.admin_user.last_name)
        self.assertEqual(response_json[0]["fields"]["email"], self.admin_user.email)
        self.assertIsNone(response_json[0]["fields"]["password"])

    def test_get_user_details(self):
        """Test retrieving a single user account."""
        self.client.force_login(user=self.admin_user)
        response = self.client.get(
            "/api/accounts/getSingle",
            {
                "id": self.admin_user.id
            },
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertEqual(response_json["username"], self.admin_user.username)
        self.assertEqual(response_json["first_name"], self.admin_user.first_name)
        self.assertEqual(response_json["last_name"], self.admin_user.last_name)
        self.assertEqual(response_json["email"], self.admin_user.email)
        self.assertEqual(response_json["mobile_number"], self.admin_user.profile.mobile_number)
        self.assertEqual(response_json["is_active"], self.admin_user.is_active)
        self.assertEqual(response_json["is_staff"], self.admin_user.is_staff)

    @mock.patch("authentication.models.Profile.send_welcome_email")
    def test_create_new_user(self, send_welcome_email_mock):
        """Test create a new user account."""
        self.client.force_login(user=self.admin_user)
        response = self.client.post(
            "/api/accounts/add",
            {
                "username": "randomname",
                "first_name": "firstname",
                "last_name": "lastname",
                "email": "sample@email.com",
                "mobile_number": "+441234566",
                "is_staff": True,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()
        new_user_id = response_json["user"]

        send_welcome_email_mock.assert_called_once()
        response = self.client.get(
            "/api/accounts/getSingle",
            {
                "id": new_user_id
            },
        )
        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertEqual(response_json["username"], "randomname")
        self.assertEqual(response_json["first_name"], "firstname")
        self.assertEqual(response_json["last_name"], "lastname")
        self.assertEqual(response_json["email"], "sample@email.com")

    def test_update_existing_user(self):
        """Test update an existing user account."""
        self.client.force_login(user=self.admin_user)
        response = self.client.post(
            "/api/accounts/update",
            {
                "id": self.admin_user.pk,
                "username": "updatedname",
                "first_name": "firstname",
                "last_name": "lastname",
                "email": "updated@email.com",
                "mobile_number": "+4412345667",
                "is_staff": True,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertTrue(response_json['success'])

        response = self.client.get(
            "/api/accounts/getSingle",
            {
                "id": self.admin_user.id
            },
        )
        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertEqual(response_json["username"], "updatedname")
        self.assertEqual(response_json["first_name"], "firstname")
        self.assertEqual(response_json["last_name"], "lastname")
        self.assertEqual(response_json["email"], "updated@email.com")
        self.assertEqual(response_json["mobile_number"], "+4412345667")
        self.assertEqual(response_json["is_staff"], True)

    def test_activate_existing_user(self):
        """Test activate an existing user account."""
        self.client.force_login(user=self.super_user)
        response = self.client.post(
            "/api/accounts/activate",
            {
                "id": self.admin_user.id,
                "is_active": False,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertTrue(response_json["success"])

        self.admin_user.refresh_from_db()
        self.assertFalse(self.admin_user.is_active)
        self.admin_user.is_active = True

    @mock.patch("authentication.models.Profile.send_welcome_email")
    def test_resend_welcome_email(self, send_welcome_email_mock):
        """Test resending the welcome email."""
        self.client.force_login(user=self.admin_user)
        response = self.client.post(
            "/api/accounts/resendEmail",
            {
                "id": self.admin_user.id,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertTrue(response_json["success"])

        send_welcome_email_mock.assert_called_once()

    def test_delete_user(self):
        """Test delete an existing user account."""
        self.client.force_login(user=self.super_user)
        response = self.client.post(
            "/api/accounts/delete",
            {
                "id": self.admin_user.id,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertTrue(response_json["success"])


class TestUserActivateAndDeleteIntegrationTesting(TestCase):
    """Test user cannot deactivate or delete its own account."""

    def setUp(self):
        self.admin_user = UserFactory(is_staff=True)

    def test_activate_existing_user(self):
        """Test that the same user cannot activate or deactivate his/her own account."""
        self.client.force_login(user=self.admin_user)
        response = self.client.post(
            "/api/accounts/activate",
            {
                "id": self.admin_user.id,
                "is_active": False,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertFalse(response_json["success"])

    def test_delete_user(self):
        """Test that the same user cannot delete his/her own account."""
        self.client.force_login(user=self.admin_user)
        response = self.client.post(
            "/api/accounts/delete",
            {
                "id": self.admin_user.id,
            }
        )

        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()

        self.assertFalse(response_json["success"])


class TestAccessAccountsIntegrationTesting(TestCase):
    """Test access to accounts api url integration tests."""

    def setUp(self):
        self.super_user = UserFactory(is_superuser=True, is_staff=True)
        self.user = UserFactory()

    def test_list_user_accounts(self):
        """Test access denied for all user accounts."""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/accounts/getAll"
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_get_user_details(self):
        """Test access denied for retrieving a single user account."""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/accounts/getSingle",
            {
                "id": self.user.id
            },
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_create_new_user(self):
        """Test access denied for create a new user account."""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/api/accounts/add",
            {
                "username": "randomname",
                "first_name": "firstname",
                "last_name": "lastname",
                "email": "sample@email.com",
                "mobile_number": "+441234566",
                "is_staff": True,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_update_existing_user(self):
        """Test access denied for update an existing user account."""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/api/accounts/update",
            {
                "id": self.user.pk,
                "username": "updatedname",
                "first_name": "firstname",
                "last_name": "lastname",
                "email": "updated@email.com",
                "mobile_number": "+4412345667",
                "is_staff": True,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_activate_existing_user(self):
        """Test access denied for activate an existing user account."""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/api/accounts/activate",
            {
                "id": self.user.id,
                "is_active": False,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_resend_welcome_email(self):
        """Test access denied for resending the welcome email."""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/api/accounts/resendEmail",
            {
                "id": self.user.id,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_delete_user(self):
        """Test access denied for delete an existing user account."""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/api/accounts/delete",
            {
                "id": self.user.id,
            }
        )

        self.assertEqual(
            response.status_code,
            302
        )
