"""API integration roles tests."""

from django.test import TestCase
from api.tests.integration import UserFactory, RoleFactory


class TestRoleIntegrationTestCase(TestCase):
    """Test ChurchRole model integration tests."""
    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.role = RoleFactory()

    def test_listing_roles(self):
        """Test that an authenticated user can list all roles"""
        self.client.force_login(user=self.user)

        response = self.client.get("/api/roles/getAll")

        self.assertEqual(
            response.status_code,
            200
        )

        response_json = response.json()

        self.assertEqual(self.role.name, response_json[0]['fields']['name'])
        self.assertEqual(self.role.description, response_json[0]['fields']['description'])

    def test_get_role(self):
        """Test that an authenticated user can get a role"""
        self.client.force_login(user=self.user)
        response = self.client.get("/api/roles/getSingle", {"id": self.role.id})

        self.assertEqual(
            response.status_code,
            200
        )

        response_json = response.json()

        self.assertEqual(self.role.name, response_json[0]['fields']['name'])
        self.assertEqual(self.role.description, response_json[0]['fields']['description'])

    def test_create_role(self):
        """Test that an authenticated user can create a role"""
        self.client.force_login(user=self.admin_user)
        new_role = RoleFactory()
        response = self.client.post(
            "/api/roles/add",
            {
                "name": new_role.name,
                "description": new_role.description,
             }
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_update_role(self):
        """Test that an authenticated user can update a role"""
        self.client.force_login(user=self.admin_user)
        new_role = RoleFactory()
        response = self.client.post(
            "/api/roles/add",
            {
                "id": self.role.id,
                "name": new_role.name,
                "description": new_role.description,
             }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_delete_role(self):
        """Test that an authenticated user can delete a role"""
        self.client.force_login(user=self.admin_user)

        response = self.client.post(
            "/api/roles/delete",
            {
                "id": self.role.id,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_get_members_by_role(self):
        """Test that an authenticated user can list members by their role"""
        self.client.force_login(user=self.user)

        response = self.client.get("/api/roles/getMembers", {"id": self.role.id})

        self.assertEqual(
            response.status_code,
            200
        )

    def test_not_authenticated_list_roles(self):
        """Test that a not authenticated user cannot list all roles"""
        response = self.client.get("/api/roles/getAll")

        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_get_single_role(self):
        """Test that a not authenticated user cannot get a role"""
        response = self.client.get("/api/roles/getSingle", {"id": self.role.id})

        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_create_role(self):
        """Test that a not authenticated user cannot crate a role"""
        new_role = RoleFactory()
        response = self.client.post(
            "/api/roles/add",
            {
                "name": new_role.name,
                "description": new_role.description,
             }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_delete_role(self):
        """Test that a not authenticated user cannot delete a role"""
        response = self.client.post(
            "/api/roles/delete",
            {
                "id": self.role.id,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_update_role(self):
        """Test that a non authenticated user cannot update a role"""
        new_role = RoleFactory()
        response = self.client.post(
            "/api/roles/add",
            {
                "id": self.role.id,
                "name": new_role.name,
                "description": new_role.description,
             }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_get_members_by_role(self):
        """Test that a not authenticated user cannot list members by their role"""
        response = self.client.get("/api/roles/getMembers", {"id": self.role.id})

        self.assertEqual(
            response.status_code,
            302
        )

    def test_non_staff_create_role(self):
        """Test that a non staff user cannot crate a role"""
        self.client.force_login(user=self.user)

        new_role = RoleFactory()
        response = self.client.post(
            "/api/roles/add",
            {
                "name": new_role.name,
                "description": new_role.description,
             }
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_non_staff_delete_role(self):
        """Test that a non staff user cannot delete a role"""
        self.client.force_login(user=self.user)
        response = self.client.post(
            "/api/roles/delete",
            {
                "id": self.role.id,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_non_staff_update_role(self):
        """Test that a non staff user cannot update a role"""
        self.client.force_login(user=self.user)
        new_role = RoleFactory()
        response = self.client.post(
            "/api/roles/add",
            {
                "id": self.role.id,
                "name": new_role.name,
                "description": new_role.description,
             }
        )
        self.assertEqual(
            response.status_code,
            302
        )