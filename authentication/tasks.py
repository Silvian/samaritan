"""
@author: Silvian Dragan
@Date: 16/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Celery tasks.
"""

from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils.timezone import now
from django_common.auth_backends import User

from samaritan.celery import app
from emailservice.models import PasswordResetEmailConfiguration, ChurchEmailConfiguration
from emailservice.mail import send_password_email

logger = get_task_logger(__name__)


@app.task
def send_email(user_id, site_url, temp_passwd):
    """Send forgot password email to reset password."""
    email_config = ChurchEmailConfiguration.load()
    password_reset = PasswordResetEmailConfiguration.load()

    if password_reset.send_email and password_reset.email_subject and password_reset.email_message:
        user = User.objects.get(id=user_id)
        send_password_email(
            sender_email=email_config.church_email,
            sender_name=email_config.church_signature,
            recipient_first_name=user.first_name,
            recipient_email=user.email,
            subject=password_reset.email_subject,
            message=password_reset.email_message,
            username=user.username,
            password=temp_passwd,
            domain=site_url,
        )
        logger.info("Sending email to: {}".format(user.email))
        logger.info("Site domain url: {}".format(site_url))


@app.task
def password_expiry():
    """Reset passwords for all users over configured number of days."""
    users = User.objects.all()

    def threshold_delta():
        if user.profile.password_last_updated:
            time_passed = now() - user.profile.password_last_updated
            seconds_passed = time_passed.total_seconds()
            days_passed = round(seconds_passed / 60 / 60 / 24)
            logger.info("Days passed since last password change: {}".format(days_passed))
            if days_passed > settings.PASSWORD_RESET_THRESHOLD:
                return True
        return False

    for user in users:
        if user.profile.password_last_updated is None or threshold_delta():
            user.profile.password_reset = True
            user.save()
            logger.info("Password expired for: {}".format(user.username))