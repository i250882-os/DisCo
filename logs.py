import logging

COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[1;31m",
}
RESET = "\033[0m"

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, "")
        record.msg = f"{color}{record.msg}{RESET}"
        return super().format(record)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter("%(levelname)s | %(message)s"))

logger.addHandler(handler)

