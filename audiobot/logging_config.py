import logging
from utils.colors import foreground

fcl = foreground()
RESET = fcl.RESET


class CustomFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: fcl.BBLUE_FG,
        logging.INFO: fcl.GREEN_FG,
        logging.WARNING: fcl.YELLOW_FG,
        logging.ERROR: fcl.RED_FG,
        logging.CRITICAL: fcl.MAGENTA_FG,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, fcl.WHITE_FG)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET}"


def setup_colored_logger(logger_name="colored_logger") -> logging.Logger:
    """
    Sets up a colored logger with a single handler.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger(logger_name)

    if not logger.handlers:  # Check if handlers already exist
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter("- %(levelname)s - %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    # Prevent log messages from propagating to the root logger.
    logger.propagate = False

    return logger
