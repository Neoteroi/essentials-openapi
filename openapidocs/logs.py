import logging

from rich.logging import RichHandler

logger = logging.getLogger("openapidocs")
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler())
