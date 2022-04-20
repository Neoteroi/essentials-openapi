import logging
import logging.handlers

try:
    from rich.logging import RichHandler
except ImportError:
    RichHandler = None

logger = logging.getLogger("openapidocs")
logger.setLevel(logging.INFO)

if RichHandler is None:
    logger.addHandler(logging.StreamHandler())
else:
    logger.addHandler(RichHandler())
