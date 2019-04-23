"""API integration tests factories."""

import factory
from django_common.auth_backends import User

from factory.django import DjangoModelFactory
from samaritan.models import Address, ChurchRole, MembershipType, ChurchGroup, Member


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = factory.Faker('name')
    
    class Meta:
        model = User


class AddressFactory(DjangoModelFactory):
    """Factory for address."""

    number = factory.Faker('word')
    street = factory.Faker('name')
    locality = factory.Faker('name')
    city = factory.Faker('name')
    post_code = factory.Faker('word')

    class Meta:
        model = Address


class RoleFactory(DjangoModelFactory):
    """Factory for Roles."""

    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = ChurchRole


class GroupFactory(DjangoModelFactory):
    """Factory for Groups."""

    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = ChurchGroup

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if create and extracted:
            for member in extracted:
                self.members.add(member)


class MembershipTypeFactory(DjangoModelFactory):
    """Membership Type Factory."""

    name = factory.Faker('name')
    description = factory.Faker('text')

    class Meta:
        model = MembershipType


class MemberFactory(DjangoModelFactory):
    """Factory for Members."""

    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    date_of_birth = factory.Faker('date_this_century')
    telephone = factory.Faker('random_int', min=0, max=99999999)
    address = factory.SubFactory(AddressFactory)
    email = factory.Faker('email')
    details = factory.Faker('text')
    is_baptised = factory.Faker('boolean')
    baptismal_date = factory.Faker('date_this_century')
    baptismal_place = factory.Faker('name')
    is_member = factory.Faker('boolean')
    membership_type = factory.SubFactory(MembershipTypeFactory)
    membership_date = factory.Faker('date_this_year')
    is_active = factory.Faker('boolean')
    notes = factory.Faker('text')
    church_role = factory.SubFactory(RoleFactory)
    gdpr = factory.Faker('boolean')

    class Meta:
        model = Member
