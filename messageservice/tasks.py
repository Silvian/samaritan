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
        message = message.encode('utf-8')
        logger.info('Sending:"{}" to: {}'.format(message, phone))
        response = SMSService().send_sms(message, phone)
        if response.get('success'):
            sms_config.counter += 1
            sms_config.save()
            logger.info("Successfully sent message to: {}".format(phone))
        else:
            logger.error("Failed to send sms to the following mobile number: {}".format(phone))
            logger.error("Service error: {}".format(response))
