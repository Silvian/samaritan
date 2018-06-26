"""API integration tests factories."""

import factory
from django_common.auth_backends import User

from factory.django import DjangoModelFactory
from samaritan.models import Address


class UserFactory(DjangoModelFactory):
    """Factory for users."""

    username = factory.Faker('name')

    class Meta:
        model = User


class AddressFactory(DjangoModelFactory):
    """Factory for address."""

    number = factory.Faker('text')
    street = factory.Faker('text')
    locality = factory.Faker('text')
    city = factory.Faker('text')
    post_code = factory.Faker('text')

    class Meta:
        model = Address
