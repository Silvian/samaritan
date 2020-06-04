# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import mock
import factory

from django.conf import settings
from django.test import TestCase
from factory.django import DjangoModelFactory

from api.tests.integration import MembershipTypeFactory, RoleFactory, MemberFactory
from samaritan.models import Member, Address
from webhook.models import WebhookConfiguration


class WebhookConfigurationFactory(DjangoModelFactory):
    """Factory  for WebhookConfiguration model."""

    default_role = factory.SubFactory(RoleFactory)
    default_membership_type = factory.SubFactory(MembershipTypeFactory)
    enabled = True

    class Meta:
        model = WebhookConfiguration


class TestCreateMemberWebhook(TestCase):
    """Test create member webhook api."""

    @classmethod
    def setUpTestData(cls):
        cls.configuration = WebhookConfigurationFactory()
        cls.client_key = settings.WEBHOOK_API_KEY
        cls.member = MemberFactory(gdpr=True)

    @mock.patch("webhook.tasks.send_webhook_notification.delay")
    def test_create_member_webhook(self, send_webhook_notification_mock):
        extra = {"HTTP_API_KEY": self.client_key}
        response = self.client.post(
            path="/webhook/create/member",
            data=json.dumps({
                "first_name": self.member.first_name,
                "last_name": self.member.last_name,
                "date_of_birth": self.member.date_of_birth.strftime("%Y-%m-%d"),
                "telephone": self.member.telephone,
                "email": self.member.email,
                "address_no": self.member.address.number,
                "address_street": self.member.address.street,
                "address_locality": self.member.address.locality,
                "address_city": self.member.address.city,
                "address_postcode": self.member.address.post_code,
                "is_baptised": self.member.is_baptised,
                "baptismal_date": self.member.baptismal_date.strftime("%Y-%m-%d"),
                "baptismal_place": self.member.baptismal_place,
                "gdpr": self.member.gdpr,
            }),
            content_type="application/json",
            **extra
        )
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, Member.objects.count())
        self.assertEqual(2, Address.objects.count())
        created_member = Member.objects.last()
        send_webhook_notification_mock.assert_called_once_with(created_member.id)

    def test_create_member_webhook_unauthorised(self):
        response = self.client.post(
            path="/webhook/create/member",
            data=json.dumps({
                "first_name": self.member.first_name,
                "last_name": self.member.last_name,
                "date_of_birth": self.member.date_of_birth.strftime("%Y-%m-%d"),
                "telephone": self.member.telephone,
                "email": self.member.email,
                "address_no": self.member.address.number,
                "address_street": self.member.address.street,
                "address_locality": self.member.address.locality,
                "address_city": self.member.address.city,
                "address_postcode": self.member.address.post_code,
                "is_baptised": self.member.is_baptised,
                "baptismal_date": self.member.baptismal_date.strftime("%Y-%m-%d"),
                "baptismal_place": self.member.baptismal_place,
                "gdpr": self.member.gdpr,
            }),
            content_type="application/json",
        )
        self.assertEqual(403, response.status_code)

    def test_create_member_webhook_disabled(self):
        self.configuration.enabled = False
        self.configuration.save()
        extra = {"HTTP_API_KEY": self.client_key}
        response = self.client.post(
            path="/webhook/create/member",
            data=json.dumps({
                "first_name": self.member.first_name,
                "last_name": self.member.last_name,
                "date_of_birth": self.member.date_of_birth.strftime("%Y-%m-%d"),
                "telephone": self.member.telephone,
                "email": self.member.email,
                "address_no": self.member.address.number,
                "address_street": self.member.address.street,
                "address_locality": self.member.address.locality,
                "address_city": self.member.address.city,
                "address_postcode": self.member.address.post_code,
                "is_baptised": self.member.is_baptised,
                "baptismal_date": self.member.baptismal_date.strftime("%Y-%m-%d"),
                "baptismal_place": self.member.baptismal_place,
                "gdpr": self.member.gdpr,
            }),
            content_type="application/json",
            **extra
        )
        self.assertEqual(404, response.status_code)

    def test_create_member_webhook_invalid_address(self):
        extra = {"HTTP_API_KEY": self.client_key}
        response = self.client.post(
            path="/webhook/create/member",
            data=json.dumps({
                "first_name": self.member.first_name,
                "last_name": self.member.last_name,
                "date_of_birth": self.member.date_of_birth.strftime("%Y-%m-%d"),
                "telephone": self.member.telephone,
                "email": self.member.email,
                "address_no": self.member.address.number,
                "address_street": None,
                "address_locality": self.member.address.locality,
                "address_city": None,
                "address_postcode": None,
                "is_baptised": self.member.is_baptised,
                "baptismal_date": self.member.baptismal_date.strftime("%Y-%m-%d"),
                "baptismal_place": self.member.baptismal_place,
                "gdpr": self.member.gdpr,
            }),
            content_type="application/json",
            **extra
        )
        self.assertEqual(400, response.status_code)

    def test_create_member_webhook_invalid_member(self):
        extra = {"HTTP_API_KEY": self.client_key}
        response = self.client.post(
            path="/webhook/create/member",
            data=json.dumps({
                "first_name": None,
                "last_name": None,
                "date_of_birth": self.member.date_of_birth.strftime("%Y-%m-%d"),
                "telephone": self.member.telephone,
                "email": self.member.email,
                "address_no": self.member.address.number,
                "address_street": self.member.address.street,
                "address_locality": self.member.address.locality,
                "address_city": self.member.address.city,
                "address_postcode": self.member.address.post_code,
                "is_baptised": self.member.is_baptised,
                "baptismal_date": self.member.baptismal_date.strftime("%Y-%m-%d"),
                "baptismal_place": self.member.baptismal_place,
                "gdpr": self.member.gdpr,
            }),
            content_type="application/json",
            **extra
        )
        self.assertEqual(400, response.status_code)

    def test_create_member_webhook_invalid_date_format(self):
        extra = {"HTTP_API_KEY": self.client_key}
        response = self.client.post(
            path="/webhook/create/member",
            data=json.dumps({
                "first_name": None,
                "last_name": None,
                "date_of_birth": self.member.date_of_birth.strftime("%d/%m/%Y"),
                "telephone": self.member.telephone,
                "email": self.member.email,
                "address_no": self.member.address.number,
                "address_street": self.member.address.street,
                "address_locality": self.member.address.locality,
                "address_city": self.member.address.city,
                "address_postcode": self.member.address.post_code,
                "is_baptised": self.member.is_baptised,
                "baptismal_date": self.member.baptismal_date.strftime("%d/%m/%Y"),
                "baptismal_place": self.member.baptismal_place,
                "gdpr": self.member.gdpr,
            }),
            content_type="application/json",
            **extra
        )
        self.assertEqual(400, response.status_code)

    def test_create_member_webhook_bad_request(self):
        extra = {"HTTP_API_KEY": self.client_key}
        response = self.client.post(
            path="/webhook/create/member",
            data={},
            content_type="application/json",
            **extra
        )
        self.assertEqual(400, response.status_code)

