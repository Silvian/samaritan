"""
@author: Silvian Dragan
@Date: 16/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Celery tasks.
"""

from axes.models import AccessAttempt
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils.timezone import now
from django_common.auth_backends import User

from samaritan.celery import app
from emailservice.models import (
    EmailTypes,
    EmailConfiguration,
    ChurchEmailConfiguration,
)

from emailservice.mail import send_login_link_email, send_password_email

logger = get_task_logger(__name__)


@app.task
def send_login_link(user_id, site_url, link):
    """Send forgot password email to reset password."""
    email_config = ChurchEmailConfiguration.load()
    login_link = EmailConfiguration.objects.get(type=EmailTypes.LOGIN_LINK.name)

    if login_link.send_email:
        user = User.objects.get(id=user_id)
        send_login_link_email(
            sender_email=email_config.church_email,
            sender_name=email_config.church_signature,
            recipient_first_name=user.first_name,
            recipient_email=user.email,
            subject=login_link.subject,
            message=login_link.message,
            link=link,
            domain=site_url,
        )
        logger.info("Sending email to: {}".format(user.email))
        logger.info("Site domain url: {}".format(site_url))

@app.task
def send_reset_email(user_id, site_url, temp_passwd):
    """Send forgot password email to reset password."""
    email_config = ChurchEmailConfiguration.load()
    password_reset = EmailConfiguration.objects.get(type=EmailTypes.PASSWORD_RESET.name)

    if password_reset.send_email:
        user = User.objects.get(id=user_id)
        send_password_email(
            sender_email=email_config.church_email,
            sender_name=email_config.church_signature,
            recipient_first_name=user.first_name,
            recipient_email=user.email,
            subject=password_reset.subject,
            message=password_reset.message,
            username=user.username,
            password=temp_passwd,
            domain=site_url,
        )
        logger.info("Sending email to: {}".format(user.email))
        logger.info("Site domain url: {}".format(site_url))


@app.task
def send_welcome_pack(user_id, site_url, temp_passwd):
    """Send the user's welcome pack email when a new user is created."""
    email_config = ChurchEmailConfiguration.load()
    welcome_email = EmailConfiguration.objects.get(type=EmailTypes.WELCOME_EMAIL.name)

    if welcome_email.send_email:
        user = User.objects.get(id=user_id)
        send_password_email(
            sender_email=email_config.church_email,
            sender_name=email_config.church_signature,
            recipient_first_name=user.first_name,
            recipient_email=user.email,
            subject=welcome_email.subject,
            message=welcome_email.message,
            username=user.username,
            password=temp_passwd,
            domain=site_url,
        )
        logger.info("Sending welcome pack to: {}".format(user.email))
        logger.info("Site domain url: {}".format(site_url))


@app.task
def check_user_lockout():
    """Check axes lockout for any user and deactivate the user account."""
    from authentication.models import MFACode
    queryset = AccessAttempt.objects.filter(
        failures_since_start__gte=settings.AXES_FAILURE_LIMIT
    )
    attempt_users = queryset.values_list('username', flat=True)
    if attempt_users:
        deactivate_users = User.objects.filter(username__in=attempt_users)
        for user in deactivate_users:
            user.is_active = False
            user.save()
            logger.info("Deactivated user: {}".format(user.username))

    attempt_tokens = queryset.filter(username__isnull=True, path_info__isnull=False)
    if attempt_tokens:
        tokens = []
        for token in attempt_tokens:
            tokens.append(token.path_info.split('/')[3])

        deactivate_codes = MFACode.objects.filter(token__in=tokens)
        for code in deactivate_codes:
            user = code.user
            user.is_active = False
            user.save()
            logger.info("Deactivated user: {}".format(user.username))
