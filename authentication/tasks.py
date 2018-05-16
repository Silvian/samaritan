"""
@author: Silvian Dragan
@Date: 16/05/2018
@Copyright: Copyright 2018, Samaritan CMA - Published under GNU General Public Licence v3
@Details: https://github.com/Silvian/samaritan

Celery tasks.
"""

from celery.utils.log import get_task_logger
from django_common.auth_backends import User

from samaritan.celery import app

logger = get_task_logger(__name__)


@app.task
def send_email(user_id, site_url, temp_passwd):
    """Send forgot password email to reset password."""
    logger.info("User ID: {}".format(user_id))          # TODO: REMOVE THIS
    logger.info("Temp passwd: {}".format(temp_passwd))  # TODO: REMOVE THIS
    user = User.objects.get(id=user_id)
    logger.info("Sending email to: {}".format(user.email))
    logger.info("Site domain url: {}".format(site_url))
    # TODO: Actually send the damn email
