import logging
from logging.handlers import RotatingFileHandler

from config import LOG_FILE_NAME


class SuppressBSONFilter(logging.Filter):
    def filter(self, record):
        return "bson.errors.InvalidDocument" not in record.getMessage()


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=5000000, backupCount=10),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger()
logger.addFilter(SuppressBSONFilter())

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)

# Setting ntgcalls logger level and disabling propagation
ntgcalls_logger = logging.getLogger("ntgcalls")
ntgcalls_logger.setLevel(logging.CRITICAL)
ntgcalls_logger.propagate = False


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
