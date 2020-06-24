import logging

logging.basicConfig(level=logging.INFO)
logging.info('info')

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.debug('debug')
    return logger
