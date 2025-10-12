"""
Logging configuration for Filemac.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    format_string: Optional[str] = None,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Setup logging configuration for kcleaner.

    Args:
        level: Logging level
        format_string: Custom format string
        log_file: Optional log file path

    Returns:
        Configured logger
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    formatter = logging.Formatter(format_string)

    # Root logger
    logger = logging.getLogger("filemac")
    logger.setLevel(level)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


class LoggingContext:
    """Context manager for temporary logging configuration."""

    def __init__(self, level: int = logging.INFO, log_file: Optional[str] = None):
        self.level = level
        self.log_file = log_file
        self.original_level = None
        self.file_handler = None

    def __enter__(self):
        self.original_level = logging.getLogger("filemac").level
        setup_logging(level=self.level, log_file=self.log_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        setup_logging(level=self.original_level)
        if self.file_handler:
            logging.getLogger("filemac").removeHandler(self.file_handler)
