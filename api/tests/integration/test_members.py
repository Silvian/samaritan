"""API integration members tests."""

from django.test import TestCase
from api.tests.integration import UserFactory, MemberFactory


class TestMemberIntegrationTestCase(TestCase):

    def setUp(self):
        self.user = UserFactory(is_superuser=True)
        self.admin_user = UserFactory(is_staff=True)
        self.member = MemberFactory()

    def test_add_member(self):
        """ Test that an admin user can add a new member"""
        self.client.force_login(user=self.admin_user)
        new_member = MemberFactory()   
        response = self.client.post(
            '/api/members/add',
            {
                "first_name": new_member.first_name,
                "last_name": new_member.last_name,
                "date_of_birth": new_member.date_of_birth,
                "telephone": new_member.telephone,
                "address": new_member.address.id,
                "email": new_member.email,
                "details": new_member.details,
                "is_baptised": new_member.is_baptised,
                "baptismal_date": new_member.baptismal_date,
                "baptismal_place": new_member.baptismal_place,
                "is_member": new_member.is_member,
                "membership_type": new_member.membership_type.id,
                "membership_date": new_member.membership_date,
                "is_active": new_member.is_active,
                "church_role": new_member.church_role.id,
                "gdpr": new_member.gdpr,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_update_member(self):
        """Test that an admin user can update a member"""
        self.client.force_login(user=self.admin_user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/update",
            {
                "id": self.member.id, 
                "first_name": new_member.first_name,
                "last_name": new_member.last_name,
                "date_of_birth": new_member.date_of_birth,
                "telephone": new_member.telephone,
                "address": new_member.address.id,
                "email": new_member.email,
                "details": new_member.details,
                "is_baptised": new_member.is_baptised,
                "baptismal_date": new_member.baptismal_date,
                "baptismal_place": new_member.baptismal_place,
                "is_member": new_member.is_member,
                "membership_type": new_member.membership_type.id,
                "membership_date": new_member.membership_date,
                "is_active": new_member.is_active,
                "church_role": new_member.church_role.id,
                "gdpr": new_member.gdpr,
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_delete_member(self):
        """Test that an admin user can delete a member"""
        self.client.force_login(user=self.admin_user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/delete",
            {
                "id": new_member.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_terminate_member(self):
        """Test that an admin user can terminate a member"""
        self.client.force_login(user=self.admin_user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/terminate",
            {
                "id": new_member.id,
                "notes": new_member.notes
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_reinstate_member(self):
        """Test that an admin user can reinstate a member"""

        self.client.force_login(user=self.admin_user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/reinstate",
            {
                "id": new_member.id
            }
        )
        self.assertEqual(
            response.status_code,
            200
        )

    def test_list_active_members(self):
        """Test that an authenticated user can list all active members"""
        self.client.force_login(user=self.user)
        response = self.client.get(
            "/api/members/getActive"
        )
        self.assertEqual(
            response.status_code,
            200
        )
   
    def test_get_member(self):
        """Test that an authenticated user can list a member"""
        self.client.force_login(user=self.user)
        new_member = MemberFactory()
        response = self.client.get(
            "/api/members/getMember",
            {"id": new_member.id}
        )
        self.assertEqual(
            response.status_code,
            200
        )
        response_json = response.json()
        self.assertEqual(
            response_json[0]['pk'],
            new_member.id
        )
        
    def test_not_authenticated_add_member(self):
        """ Test that a non-admin user cannot add a new member"""
        self.client.force_login(user=self.user)
        new_member = MemberFactory()   
        response = self.client.post(
            '/api/members/add',
            {
                "first_name": new_member.first_name,
                "last_name": new_member.last_name,
                "date_of_birth": new_member.date_of_birth,
                "telephone": new_member.telephone,
                "address": new_member.address.id,
                "email": new_member.email,
                "details": new_member.details,
                "is_baptised": new_member.is_baptised,
                "baptismal_date": new_member.baptismal_date,
                "baptismal_place": new_member.baptismal_place,
                "is_member": new_member.is_member,
                "membership_type": new_member.membership_type.id,
                "membership_date": new_member.membership_date,
                "is_active": new_member.is_active,
                "church_role": new_member.church_role.id,
                "gdpr": new_member.gdpr,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_update_member(self):
        """Test that a non-admin user cannot update a member"""
        self.client.force_login(user=self.user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/update",
            {
                "id": self.member.id, 
                "first_name": new_member.first_name,
                "last_name": new_member.last_name,
                "date_of_birth": new_member.date_of_birth,
                "telephone": new_member.telephone,
                "address": new_member.address.id,
                "email": new_member.email,
                "details": new_member.details,
                "is_baptised": new_member.is_baptised,
                "baptismal_date": new_member.baptismal_date,
                "baptismal_place": new_member.baptismal_place,
                "is_member": new_member.is_member,
                "membership_type": new_member.membership_type.id,
                "membership_date": new_member.membership_date,
                "is_active": new_member.is_active,
                "church_role": new_member.church_role.id,
                "gdpr": new_member.gdpr,
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_delete_member(self):
        """Test that a non-admin user cannot delete a member"""
        self.client.force_login(user=self.user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/delete",
            {
                "id": new_member.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_terminate_member(self):
        """Test that a non-admin user cannot terminate a member"""
        self.client.force_login(user=self.user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/terminate",
            {
                "id": new_member.id,
                "notes": new_member.notes
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_reinstate_member(self):
        """Test that a non-admin user cannot reinstate a member"""
        self.client.force_login(user=self.user)
        new_member = MemberFactory()
        response = self.client.post(
            "/api/members/reinstate",
            {
                "id": new_member.id
            }
        )
        self.assertEqual(
            response.status_code,
            302
        )

    def test_not_authenticated_list_active_members(self):
        """Test that a non-authenticated user cannot list all active members"""
        response = self.client.get(
            "/api/members/getActive"
        )
        self.assertEqual(
            response.status_code,
            302
        )
   
    def test_not_authenticated_get_member(self):
        """Test that a non-authenticated user cannot list a member"""
        new_member = MemberFactory()
        response = self.client.get(
            "/api/members/getMember",
            {"id": new_member.id}
        )
        self.assertEqual(
            response.status_code,
            302
        )
