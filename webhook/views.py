# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError
from django.db.transaction import atomic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from samaritan.models import Member, Address
from webhook.decorators import api_key_required
from webhook.models import WebhookConfiguration
from webhook.tasks import send_webhook_notification


@atomic
@csrf_exempt
@api_key_required
def create_member_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        config = WebhookConfiguration.load()
        if not config.enabled:
            return HttpResponse(status=404)

        try:
            address = Address.objects.create(
                number=data.get('address_no') or None,
                street=data.get('address_street') or None,
                locality=data.get('address_locality') or None,
                city=data.get('address_city') or None,
                post_code=data.get('address_postcode') or None,
            )
        except (DatabaseError, IntegrityError, ValidationError):
            return HttpResponse(status=400)

        try:
            member = Member.objects.create(
                first_name=data.get('first_name') or None,
                last_name=data.get('last_name') or None,
                date_of_birth=data.get('date_of_birth') or None,
                telephone=data.get('telephone') or None,
                email=data.get('email') or None,
                address=address,
                is_baptised=data.get('is_baptised') or False,
                baptismal_date=data.get('baptismal_date') or None,
                baptismal_place=data.get('baptismal_place') or None,
                is_member=False,
                membership_type=config.default_membership_type,
                is_active=True,
                church_role=config.default_role,
                gdpr=data.get('gdpr') or False,

            )
        except (DatabaseError, IntegrityError, ValidationError):
            return HttpResponse(status=400)

        if member:
            send_webhook_notification.delay(member.id)
            return HttpResponse(status=201)

    return HttpResponse(status=400)
