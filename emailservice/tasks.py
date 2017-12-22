"""
@author: Silvian Dragan
@Date: 12/12/2017
@Copyright: Copyright 2017, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Celery tasks.
"""
from datetime import date

from celery.utils.log import get_task_logger

from samaritan.celery import app
from samaritan.models import Member, ChurchGroup
from emailservice.mail import send_email, send_list_email
from emailservice.models import (
    ChurchEmailConfiguration,
    BirthdayEmailGreetingConfiguration,
    BirthdaysListConfiguration,
    GroupRotationConfiguration,
)


logger = get_task_logger(__name__)


@app.task
def send_email_task(from_email, from_name, subject, message, member_first_name, member_last_name, member_email):
    """Send batch emails task."""
    logger.info("Sending email to: {} {}".format(member_last_name, member_first_name))
    if not send_email(from_email, from_name, member_first_name,
                      member_email, subject, message):
        logger.warn("Failed to send email to the following recipient: {}".format(member_email))


@app.task
def send_birthday_greeting():
    """Send birthday greeting to members."""
    email_config = ChurchEmailConfiguration.load()
    birthday_config = BirthdayEmailGreetingConfiguration.load()
    logger.info("Running send birthday greeting task...")

    # get everyone from members list including guests
    everyone = Member.objects.filter(is_active=True)

    # get today's date
    today = date.today()

    if birthday_config.send_emails and birthday_config.subject and birthday_config.greeting:

        for member in everyone:

            # check each member's date of birth matches current day and month
            if member.date_of_birth.month == today.month and member.date_of_birth.day == today.day \
                    and member.date_of_birth.year > birthday_config.threshold:
                logger.info("Sending greeting to: {} {}".format(member.last_name, member.first_name))
                if member.email is not None and member.email != "":
                    if not send_email(email_config.church_email, email_config.church_signature, member.first_name,
                                      member.email, birthday_config.subject, birthday_config.greeting):
                        logger.warn("Failed to send email to the following recipient: {}".format(member.email))


@app.task
def send_birthdays_list():
    """Send birthdays list to select role members."""
    email_config = ChurchEmailConfiguration.load()
    birthdays_list_config = BirthdaysListConfiguration.load()
    greeting_config = BirthdayEmailGreetingConfiguration.load()

    # get everyone from members list including guests
    everyone = Member.objects.filter(is_active=True)

    # get today's date
    today = date.today()

    # get last month
    last_month = today.month - 1

    if last_month == 0:
        last_month = 12

    birthdays_list = []

    if birthdays_list_config.send_emails and birthdays_list_config.subject:
        if today.day <= birthdays_list_config.week_cycle and today.weekday() == birthdays_list_config.sending_day:

            for member in everyone:
                if member.date_of_birth.month == last_month and member.date_of_birth.year > greeting_config.threshold:
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
            if not send_list_email(email_config.church_email, email_config.church_signature, recipient.first_name,
                                   recipient.email, birthdays_list_config.subject, birthdays_list):
                logger.warn("Failed to send email to the following recipient: {}".format(recipient.email))


@app.task
def group_rotation_schedule():
    """Set the next group in the rotation weekly schedule."""
    group_rotation = GroupRotationConfiguration.load()

    if group_rotation.group_number:
        if group_rotation.group_number == 4:
            group_rotation.group_number = 1
        else:
            group_rotation.group_number += 1

        logger.info("Group Rotation: {}".format(str(group_rotation.group_number)))

        group_rotation.save()


@app.task
def send_group_schedule_notification():
    """Send notification for the next group scheduled."""
    email_config = ChurchEmailConfiguration.load()
    group_rotation = GroupRotationConfiguration.load()
    group_name = "{} {}".format(group_rotation.group_name, group_rotation.group_number)

    if group_rotation.send_emails and group_rotation.email_subject and group_rotation.email_message:
        logger.debug("Group name: {}".format(group_name))
        group = ChurchGroup.objects.get(name=group_name)

        for member in group.members.order_by('last_name').filter(is_active=True):
            if member.email:
                logger.info("Sending group notification to: {} {}".format(member.last_name, member.first_name))
                if not send_email(email_config.church_email, email_config.church_signature, member.first_name,
                                  member.email, group_rotation.email_subject, group_rotation.email_message):
                    logger.warn("Failed to send email to the following recipient: {}".format(member.email))
