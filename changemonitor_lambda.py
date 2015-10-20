import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('got event{}'.format(event))
    logger.info('got contenxt{}'.format(context))
    logger.error('something went wrong')

    return 'Hello world!'
