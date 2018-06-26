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

    number = factory.Faker('word')
    street = factory.Faker('name')
    locality = factory.Faker('name')
    city = factory.Faker('name')
    post_code = factory.Faker('word')

    class Meta:
        model = Address
