from invoke import task
from os import environ
from sys import stdout

import logging
from logging.handlers import RotatingFileHandler
from library.simple_ui import SimpleUI

LOG_LEVEL = environ.get("BG_VAR_log_level", "INFO")
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s = %(message)s"
stream_handler = logging.StreamHandler(stream=stdout)
file_handler = RotatingFileHandler(
    "truth_or_dare.log",
    mode='a',
    maxBytes=5*1024*1024,
    backupCount=2,
    encoding=None,
    delay=0
)
logging.basicConfig(
    handlers=[file_handler, stream_handler],
    format=LOG_FORMAT,
    level=logging.getLevelName(LOG_LEVEL)
)

LOG = logging.getLogger(__name__)

@task
def simpletod(context):
    try:
        SimpleUI().run()
    except Exception as error:
        LOG.error(error)