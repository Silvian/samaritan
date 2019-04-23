"""
@author: Silvian Dragan
@Date: 01/01/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""
from django.core.management import BaseCommand

from samaritan.models import ChurchRole


class Command(BaseCommand):
    """creates default church role for all member types."""

    help = __doc__

    def handle(self, *args, **options):
        role, created = ChurchRole.objects.get_or_create(
            name='regular',
            defaults={
                'description': 'Regular church member role.'
            },
        )

        if created:
            print "Default role created: {}".format(role.name)

        else:
            print "Default role already exists"
