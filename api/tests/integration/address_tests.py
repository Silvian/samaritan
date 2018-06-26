"""API integration address tests."""
import factory
from django.test import TestCase
from samaritan.models import Address
from factory.django import DjangoModelFactory


class AddressModelFactory(DjangoModelFactory):
    """Factory for address"""

    number = factory.Faker('text')
    street = factory.Faker('text')
    locality = factory.Faker('text')
    post_code = factory.Faker('text')

    class Meta:
        model = Address
