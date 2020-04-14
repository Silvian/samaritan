"""
@author: Silvian Dragan
@Date: 14/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan
"""

import uuid
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django_common.auth_backends import User
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from messageservice.models import SMSMessageConfiguration
from samaritan.base_models import SingletonModel
from .tasks import send_reset_email, send_welcome_pack
from .utils import (
    PasswordGenerator,
    PasswordPwnedChecker,
    PasswordEntropyCalculator,
    RandomHashGenerator,
)


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
    profile_pic = models.ImageField(
        blank=True,
        null=True,
        default='images/guest.png',
        upload_to='profile_images',
    )
    password_strength = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    password_breached = models.BooleanField(
        default=False,
    )
    password_reset = models.BooleanField(
        default=False,
    )
    password_last_updated = models.DateTimeField(
        blank=True,
        null=True,
    )
    mfa_enabled = models.BooleanField(
        default=False,
    )

    def send_password_email(self, site_url):
        """Send email with temporary password."""
        temp_passwd = self.generate_temp_password()
        send_reset_email.delay(self.user.id, site_url, temp_passwd)

    def send_welcome_email(self, site_url):
        """Send the welcome pack email."""
        temp_passwd = self.generate_temp_password()
        send_welcome_pack.delay(self.user.id, site_url, temp_passwd)

    def generate_temp_password(self):
        """Generate temporary password."""
        self.password_reset = True
        generator = PasswordGenerator()
        passwd = generator.generate_password()
        self.user.set_password(passwd)
        self.user.save()
        return passwd

    def verify_password_strength(self, password):
        """Verify if password is strong enough."""
        entropy_cal = PasswordEntropyCalculator()
        entropy = entropy_cal.calculate(password)
        self.password_strength = entropy
        self.save()

        if entropy >= entropy_cal.threshold:
            return True

        return False

    def verify_password_breached(self, password):
        """Verify if password has been breached."""
        checker = PasswordPwnedChecker()
        if checker.pwned_check(password):
            self.password_breached = True
            self.save()
            return True

        else:
            self.password_breached = False
            self.save()
            return False

    def save(self, *args, **kwargs):
        if not self.profile_pic:
            self.profile_pic = 'images/guest.png'

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        """Return the string representation."""
        return self.user.username


class MFACode(models.Model):
    """Multi factor authentication codes."""

    token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
    expiry_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(
        default=timezone.now,
    )

    @property
    def expired(self):
        if timezone.now() > self.expiry_date:
            return True
        return False

    def calculate_six_digit_code(self):
        """Calculate six digit code."""
        six_digit_pin = str(int(self.code, 16))[:6]
        return six_digit_pin

    def __str__(self):
        """Return the string representation."""
        return self.code

    def save(self, *args, **kwargs):
        """Generate the code hash and expiry date."""
        generator = RandomHashGenerator()
        self.code = generator.generate_hash()
        self.expiry_date = timezone.now() + timedelta(
            seconds=settings.TOKEN_EXPIRY_THRESHOLD
        )
        super(MFACode, self).save(*args, **kwargs)


class MFACookie(models.Model):
    """MFA Cookies."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    expiry_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(
        default=timezone.now,
    )

    @property
    def expired(self):
        if timezone.now() > self.expiry_date:
            return True
        return False

    def __str__(self):
        """Return the string representation."""
        return str(self.id)

    def save(self, *args, **kwargs):
        """Set the expiry date."""
        self.expiry_date = timezone.now() + timedelta(
            seconds=settings.COOKIE_EXPIRY_THRESHOLD
        )
        super(MFACookie, self).save(*args, **kwargs)


class MFAConfiguration(SingletonModel):
    """MFA Configurations."""

    name = models.CharField(
        max_length=50,
        default='MFA Settings',
    )
    enabled = models.BooleanField(
        default=False,
    )

    @property
    def quota_remaining(self):
        """Get the remaining quota."""
        sms_config = SMSMessageConfiguration.load()
        if sms_config and sms_config.send_message:
            return sms_config.quota_remaining

        return 0

    @property
    def active(self):
        """Check if MFA is active."""
        if self.enabled:
            if self.quota_remaining >= settings.SMS_AVAILABILITY_THRESHOLD:
                return True

        return False

    def __str__(self):
        """Return the string representation."""
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when an user instance is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update profile when user is updated."""
    instance.profile.save()
