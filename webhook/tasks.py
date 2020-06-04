"""Webhook tasks."""

from celery.utils.log import get_task_logger

from emailservice.mail import send_webhook_email
from emailservice.models import (
    ChurchEmailConfiguration,
    EmailConfiguration,
    EmailTypes,
)
from samaritan.celery import app
from samaritan.models import Member

logger = get_task_logger(__name__)


@app.task
def send_webhook_notification(member_id):
    email_config = ChurchEmailConfiguration.load()
    webhook_email_config = EmailConfiguration.objects.get(type=EmailTypes.WEBHOOK_NOTIFICATION.name)
    member = Member.objects.get(id=member_id)
    logger.info("Sending notification for newly created member: {}".format(member))

    # get church roles from config
    recipients_list = []
    for church_role in set(webhook_email_config.recipient_roles.all()):
        role_members = Member.objects.filter(church_role=church_role, is_active=True)
        for recipient in role_members:
            recipients_list.append(recipient)

    for recipient in recipients_list:
        logger.info("Sending webhook notification email to: {} {}".format(recipient.last_name, recipient.first_name))
        if not send_webhook_email(
            sender_email=email_config.church_email,
            sender_name=email_config.church_signature,
            recipient_first_name=recipient.first_name,
            recipient_email=recipient.email,
            subject=webhook_email_config.subject,
            message=webhook_email_config.message,
            member=member,
        ):
            logger.warn("Failed to send email to the following recipient: {}".format(recipient.email))
