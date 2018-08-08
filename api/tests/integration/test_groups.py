"""API integration groups tests."""
from django.test import TestCase
from api.tests.integration import UserFactory, GroupFactory, MemberFactory

class TestGroupsIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.group = GroupFactory()
        self.member = MemberFactory()

    def test_list_all_groups(self):
        """Test that an authenticated user can list all groups"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/groups/getAll"
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_get_single_group(self):
        """Test that an authenticated user can list a group"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/groups/getSingle",
            {"id": self.group.id}
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_add_groups(self):
        """Test that an authenticated user can add a new group"""
        self.client.force_login(user=self.user)
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/add",
            {
                "name": new_group.name,
                "description": new_group.description,
                "members": new_group.members
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_update_group(self):
        """Test that an authenticated user can update a group"""
        self.client.force_login(user=self.user)
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/update",
            {
                "id": self.group.id,
                "name": new_group.name,
                "description": new_group.description,
                "members": new_group.members
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_delete_group(self):
        """Test that an authenticated user can delete a group"""
        self.client.force_login(user=self.user)
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/delete",
            {
                "id": new_group.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_get_members_group(self):
        """Test that an authenticated user can get a group's members"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/groups/getMembers",
            {
                "id": self.group.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_members_to_add(self):
        """Test that an authenticated user can add members to a group"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/groups/membersToAdd",
            {
                "id": self.group.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_member_add(self):
        """Test that an authenticated user can add a member to a group"""
        self.client.force_login(user=self.user)
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/memberAdd",
            {
                "group_id": new_group.id,
                "member_id": self.member.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
    
    def test_member_delete(self):
        """Test that an authenticated user can delete a member from a group"""
        self.client.force_login(user=self.user)
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/memberAdd",
            {
                "group_id": new_group.id,
                "member_id": self.member.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )
        response = self.client.post(
            "/api/groups/memberDelete",
            {
                "group_id": new_group.id,
                "member_id": self.member.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_not_authenticated_list_all_groups(self):
        """Test that a non-authenticated user cannot list all groups"""
        response = self.client.get(
            "/api/groups/getAll"
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_get_single_group(self):
        """Test that a non-authenticated user cannot list a group"""
        response = self.client.get(
            "/api/groups/getSingle",
            {"id": self.group.id}
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_add_groups(self):
        """Test that a non-authenticated user cannot add a new group"""
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/add",
            {
                "name": new_group.name,
                "description": new_group.description,
                "members": new_group.members
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_update_group(self):
        """Test that a non-authenticated user cannot update a group"""
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/update",
            {
                "id": self.group.id,
                "name": new_group.name,
                "description": new_group.description,
                "members": new_group.members
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_delete_group(self):
        """Test that a non-authenticated user cannot delete a group"""
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/delete",
            {
                "id": new_group.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_get_members_group(self):
        """Test that a non-authenticated user cannot get a group's members"""
        response = self.client.get(
            "/api/groups/getMembers",
            {
                "id": self.group.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_members_to_add(self):
        """Test that a non-authenticated user cannot add members to a group"""
        response = self.client.get(
            "/api/groups/membersToAdd",
            {
                "id": self.group.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_member_add(self):
        """Test that a non-authenticated user cannot add a member to a group"""
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/memberAdd",
            {
                "group_id": new_group.id,
                "member_id": self.member.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
    
    def test_not_authenticated_member_delete(self):
        """Test that a mmon-authenticated user cannot delete a member from a group"""
        new_group = GroupFactory()
        response = self.client.post(
            "/api/groups/memberAdd",
            {
                "group_id": new_group.id,
                "member_id": self.member.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
        response = self.client.post(
            "/api/groups/memberDelete",
            {
                "group_id": new_group.id,
                "member_id": self.member.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )
        