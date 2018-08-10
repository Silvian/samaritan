"""Message service tasks."""

from celery.utils.log import get_task_logger

from messageservice.service import SMSService
from samaritan.celery import app

logger = get_task_logger(__name__)


@app.task
def send_sms_task(message, phone):
    """Send batch sms task."""
    logger.info("Sending:{} to: {}".format(message, phone))
    if not SMSService().send_sms(message, phone):
        logger.error("Failed to send sms to the following mobile number: {}".format(phone))
