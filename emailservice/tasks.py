"""
@author: Silvian Dragan
@Date: 12/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Celery tasks.
"""

from datetime import date

from celery.utils.log import get_task_logger
from django.conf import settings

from samaritan.celery import app
from samaritan.models import Member
from emailservice.mail import send_email, send_list_email
from emailservice.models import (
    EmailTypes,
    EmailOutbox,
    EmailConfiguration,
    ChurchEmailConfiguration,
)


logger = get_task_logger(__name__)


@app.task
def send_email_task(outbox_id, member_id):
    """Send batch emails task."""
    email_outbox = EmailOutbox.objects.get(id=outbox_id)
    email_config = ChurchEmailConfiguration.load()
    member = Member.objects.get(id=member_id)
    logger.info("Sending email to: {} {}".format(member.last_name, member.first_name))
    if not send_email(
        sender_email=email_config.church_email,
        sender_name=email_config.church_signature,
        recipient_first_name=member.first_name,
        recipient_email=member.email,
        subject=email_outbox.subject,
        message=email_outbox.message,
        attachment=email_outbox.attachment,
    ):
        logger.warn("Failed to send email to the following recipient: {}".format(member.email))


@app.task
def send_birthday_greeting():
    """Send birthday greeting to members."""
    email_config = ChurchEmailConfiguration.load()
    birthday_config = EmailConfiguration.objects.get(type=EmailTypes.BIRTHDAY_GREETING.name)
    logger.info("Running send birthday greeting task...")

    # get everyone from members list including guests
    everyone = Member.objects.filter(is_active=True)

    # get today's date
    today = date.today()

    if birthday_config.send_email:
        for member in everyone:
            # check each member's date of birth matches current day and month
            if (
                member.date_of_birth.month == today.month
                and member.date_of_birth.day == today.day
                and member.date_of_birth.year > settings.THRESHOLD
            ):
                if member.church_role not in birthday_config.excluded_roles.all():
                    if member.email is not None and member.email != "":
                        logger.info("Sending greeting to: {} {}".format(member.last_name, member.first_name))
                        if not send_email(
                            sender_email=email_config.church_email,
                            sender_name=email_config.church_signature,
                            recipient_first_name=member.first_name,
                            recipient_email=member.email,
                            subject=birthday_config.subject,
                            message=birthday_config.message,
                        ):
                            logger.warn("Failed to send email to the following recipient: {}".format(member.email))


@app.task
def send_birthdays_list():
    """Send birthdays list to select role members."""
    email_config = ChurchEmailConfiguration.load()
    birthdays_list_config = EmailConfiguration.objects.get(type=EmailTypes.BIRTHDAY_LIST.name)
    greeting_config = EmailConfiguration.objects.get(type=EmailTypes.BIRTHDAY_GREETING.name)

    # get everyone from members list including guests
    everyone = Member.objects.filter(is_active=True)

    # get today's date
    today = date.today()

    # get last month
    last_month = today.month - 1

    if last_month == 0:
        last_month = 12

    birthdays_list = []

    if birthdays_list_config.send_email:
        if today.day <= settings.WEEK_CYCLE and today.weekday() == birthdays_list_config.scheduled_day:

            for member in everyone:
                if member.date_of_birth.month == last_month and member.date_of_birth.year > settings.THRESHOLD:
                    if member.church_role not in greeting_config.excluded_roles.all():
                        birthdays_list.append(member)

    # get church roles from config
    recipients_list = []

    for church_role in set(birthdays_list_config.recipient_roles.all()):
        role_members = Member.objects.filter(church_role=church_role, is_active=True)
        for recipient in role_members:
            recipients_list.append(recipient)

    # if the birthday list is not empty send it to all recipients from the recipient_list
    if birthdays_list:
        for recipient in recipients_list:
            logger.info("Sending birthdays list to: {} {}".format(recipient.last_name, recipient.first_name))
            if not send_list_email(
                sender_email=email_config.church_email,
                sender_name=email_config.church_signature,
                recipient_first_name=recipient.first_name,
                recipient_email=recipient.email,
                subject=birthdays_list_config.subject,
                message=birthdays_list_config.message,
                member_list=birthdays_list,
            ):
                logger.warn("Failed to send email to the following recipient: {}".format(recipient.email))
