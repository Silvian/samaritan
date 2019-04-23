"""
@author: Silvian Dragan
@Date: 01/01/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

from django.core.management import BaseCommand

from samaritan.models import MembershipType


class Command(BaseCommand):
    """Creates the membership types from the given list."""

    help = __doc__

    def handle(self, *args, **options):
        membership_types = {
            'Baptismal': 'Became member by being baptised in this church.',
            'Transfer': 'Transferred membership to this church from another church of the same faith.',
            'Testimony of faith':
                'Became member by pronouncing a testimony of faith after being baptised in a similar church.',
            'Not a member': 'Default membership type.',
        }

        for name, description in membership_types.items():

            membership_type, created = MembershipType.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                },
            )

            if created:
                print "Membership type created: {}".format(membership_type.name)

            else:
                print "Membership type already exists: {}".format(membership_type.name)
