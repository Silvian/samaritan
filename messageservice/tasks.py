"""Message service tasks."""

from celery.utils.log import get_task_logger

from messageservice.models import SMSMessageConfiguration
from messageservice.service import SMSService
from samaritan.celery import app

logger = get_task_logger(__name__)


@app.task
def send_sms_task(message, phone):
    """Send batch sms task."""
    sms_config = SMSMessageConfiguration.load()
    if sms_config.send_message:
        logger.info("Sending:{} to: {}".format(message, phone))
        response = SMSService().send_sms(message, phone)
        if response['success']:
            sms_config.counter += sms_config.counter
            sms_config.quota_remaining = response['quotaRemaining']
            sms_config.save()
            logger.info("Successfully sent message to: {}".format(phone))
        else:
            logger.error("Failed to send sms to the following mobile number: {}".format(phone))


@app.task
def get_sms_quota():
    """Get the sms quota remaining."""
    sms_config = SMSMessageConfiguration.load()
    response = SMSService().get_quota()
    if response['success']:
        logger.info("SMS Quota remaining {}".format(response['quotaRemaining']))
        sms_config.quota_remaining = response['quotaRemaining']
        sms_config.save()
    else:
        logger.error("Failed to retrieve remaining sms quota.")
