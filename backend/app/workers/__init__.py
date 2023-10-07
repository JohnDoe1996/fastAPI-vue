from celery import Celery
from celery.signals import after_setup_logger

from utils.loggers import Logging


app = Celery('tasks')
app.config_from_object('workers.celeryconfig')


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    logger.addHandler(Logging.getAccessHandler("./log/celery_worker.log"))
    logger.addHandler(Logging.getErrorHandler("./log/celery_worker.err.log"))