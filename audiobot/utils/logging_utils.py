import logging
from filemac.utils.colors import fg, rs

RESET = rs


class LoggingFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: fg.BBLUE_FG,
        logging.INFO: fg.GREEN_FG,
        logging.WARNING: fg.YELLOW_FG,
        logging.ERROR: fg.RED_FG,
        logging.CRITICAL: fg.MAGENTA_FG,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, fg.WHITE_FG)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET}"


def colored_logger(logger_name="colored_logger") -> logging.Logger:
    """
    Sets up a colored logger with a single handler.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(logger_name)

    if not logger.handlers:  # Check if handlers already exist
        handler = logging.StreamHandler()
        handler.setFormatter(LoggingFormatter("- %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    # Prevent log messages from propagating to the root logger.
    logger.propagate = False

    return logger
