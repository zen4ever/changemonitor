import os
from os.path import join, dirname
from dotenv import load_dotenv
from changemonitor.utils import check_if_changed, notify

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


CHANGEMONITOR_URL = os.environ.get('CHANGEMONITOR_URL')
CHANGEMONITOR_BUCKET = os.environ.get('CHANGEMONITOR_BUCKET')
CHANGEMONITOR_SNS_TOPIC = os.environ.get('CHANGEMONITOR_SNS_TOPIC')


def handler(event, context):
    logger.info("Got event: {event}".format(event))
    logger.info("Checking your url: {url}".format(url=CHANGEMONITOR_URL))
    diff = check_if_changed(CHANGEMONITOR_URL, CHANGEMONITOR_BUCKET)
    diff_text = "\n".join(diff)
    if diff_text:
        logger.info("Change detected")
        notify(CHANGEMONITOR_SNS_TOPIC, diff_text, CHANGEMONITOR_URL)
    else:
        logger.info("No changes detected")


if __name__ == "__main__":
    handler(None, None)
