import logging
from utils.colors import BLUE, GREEN, YELLOW, RED, MAGENTA, RESET, WHITE


class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, WHITE)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET}"


def set_logger() -> logging.Logger:
    """
    Sets up a colored logger with a single handler.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("colored_logger")

    if not logger.handlers:  # Check if handlers already exist
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter("- %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
