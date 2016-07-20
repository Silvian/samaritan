"""
@author: Silvian Dragan
@Date: 10/07/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main test file describing database model test cases for the Samaritan CMA app.
"""

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from models import Member, Address, MembershipType, ChurchRole, ChurchGroup


class MemberModelTests(TestCase):

    def setUp(self):

        Address.objects.create(number="1", street="Infinite Loop", locality="", city="Cupertino", post_code="10001")
        MembershipType.objects.create(name="Baptismal", description="Baptismal details")
        ChurchRole.objects.create(name="regular", description="Regular church member")

        address = Address.objects.get(post_code="10001")
        membership = MembershipType.objects.get(name="Baptismal")
        role = ChurchRole.objects.get(name="regular")

        Member.objects.create(first_name="John", last_name="Smith",
                              date_of_birth="2001-01-01", telephone="555-2525",
                              address=address, email="test@test.com", details="stuff to say",
                              profile_pic="", is_baptised=True, baptismal_date="2001-01-01", baptismal_place="Nowhere",
                              is_member=True, membership_type=membership, membership_date="2001-01-01", is_active=True,
                              notes="Test notes", church_role=role)

        ChurchGroup.objects.create(name="committee", description="The main committee group")

    def test_created_member(self):

        test_member = Member.objects.get(last_name="Smith")

        self.assertEqual(test_member.first_name, 'John')
        self.assertEqual(test_member.last_name, 'Smith')

    def test_created_address(self):

        test_address = Address.objects.get(post_code="10001")

        self.assertEqual(test_address.number, '1')
        self.assertEqual(test_address.street, 'Infinite Loop')
        self.assertEqual(test_address.city, 'Cupertino')

    def test_created_membership_type(self):

        test_membership_type = MembershipType.objects.get(name="Baptismal")

        self.assertEqual(test_membership_type.name, 'Baptismal')
        self.assertEqual(test_membership_type.description, 'Baptismal details')

    def test_created_role(self):
        test_role = ChurchRole.objects.get(name="regular")

        self.assertEqual(test_role.name, 'regular')
        self.assertEqual(test_role.description, 'Regular church member')

    def test_created_group(self):
        test_role = ChurchGroup.objects.get(name="committee")

        self.assertEqual(test_role.name, 'committee')
        self.assertEqual(test_role.description, 'The main committee group')
