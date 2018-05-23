"""
@author: Silvian Dragan
@Date: 14/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

import hashlib
import os

from django.db import models
from django.db.models.signals import post_save
from django_common.auth_backends import User
from django.dispatch import receiver

from .tasks import send_email


class Profile(models.Model):
    """Profile data model."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    mobile_number = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    password_reset = models.BooleanField(
        default=False,
    )
    password_last_updated = models.DateTimeField(
        blank=True,
        null=True,
    )

    def send_password_email(self, site_url):
        """Send email with temporary password."""
        temp_passwd = self.generate_temp_password()
        send_email.delay(self.user.id, site_url, temp_passwd)

    def generate_temp_password(self):
        """Generate temporary password."""
        self.password_reset = True
        passwd = hashlib.sha1(os.urandom(128)).hexdigest()
        self.user.set_password(passwd)
        self.user.save()

        return passwd

    def __str__(self):
        """Return the string representation."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when an user instance is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update profile when user is updated."""
    instance.profile.save()
