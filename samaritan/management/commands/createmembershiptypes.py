"""
@author: Silvian Dragan
@Date: 01/01/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.core.management import BaseCommand

from samaritan.models import MembershipType


class Command(BaseCommand):
    help = 'Creates the membership types from the given list.'

    def handle(self, *args, **options):
        membership_types = {
            'Baptismal': 'Became member by being baptised in this church.',
            'Transfer': 'Transferred membership to this church from another church of the same faith.',
            'Testimony of faith':
                'Became member by pronouncing a testimony of faith after being baptised in a similar church.',
        }

        for name, description in membership_types.items():

            membership_type, created = MembershipType.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                },
            )

            if created:
                print("Membership type created: ", membership_type.name)

            else:
                print("Membership type already exists: ", membership_type.name)
