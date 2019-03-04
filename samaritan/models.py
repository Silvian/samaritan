"""
@author: Silvian Dragan
@Date: 02/05/2016
@Copyright: Copyright 2016, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Main models file describing database models for the Samaritan CMA app.
"""

from django.db import models
from django.utils import timezone


class Address(models.Model):
    """Address data model."""

    number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    street = models.CharField(
        max_length=200,
    )
    locality = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=200,
    )
    post_code = models.CharField(
        max_length=50,
    )

    def publish(self):
        self.save()

    def __str__(self):
        return self.post_code


class MembershipType(models.Model):
    """MembershipType data model."""

    name = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class ChurchRole(models.Model):
    """ChurchRole data model."""

    name = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class Member(models.Model):
    """Member data model."""

    first_name = models.CharField(
        max_length=200,
    )
    last_name = models.CharField(
        max_length=200,
    )
    date_of_birth = models.DateField(

    )
    telephone = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.PROTECT,
    )
    email = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    details = models.TextField(
        blank=True,
        null=True,
    )
    profile_pic = models.ImageField(
        max_length=100,
        blank=True,   
        upload_to='profile_images_members',
        null=True
    )
    is_baptised = models.BooleanField(
        default=False,
    )
    baptismal_date = models.DateField(
        blank=True,
        null=True,
    )
    baptismal_place = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    is_member = models.BooleanField(

    )
    membership_type = models.ForeignKey(
        MembershipType,
        blank=True,
        null=True,
    )
    membership_date = models.DateField(
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )
    church_role = models.ForeignKey(
        ChurchRole,
        on_delete=models.CASCADE,
    )
    gdpr = models.BooleanField(
        default=False,
    )
    created_date = models.DateTimeField(
        default=timezone.now,
    )

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.last_name + " " + self.first_name


class ChurchGroup(models.Model):
    """ChurchGroup data model."""

    name = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    members = models.ManyToManyField(
        Member,
        blank=True,
    )

    def publish(self):
        self.save()

    def __str__(self):
        return self.name
