"""Command to create profile for existing users."""

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from authentication.models import Profile


class Command(BaseCommand):
    """create a profile object for all existing users."""

    help = __doc__

    def handle(self, *args, **options):
        """Create profile for each user."""
        users = User.objects.all()
        for user in users:
            if not Profile.objects.filter(user=user):
                Profile.objects.create(user=user)
                print "Profile created for user: {}".format(user.username)
