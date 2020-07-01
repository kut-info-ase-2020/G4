import logging

formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
