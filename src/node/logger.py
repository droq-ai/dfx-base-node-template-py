"""Optional logging helper for the node."""

import logging
import os
import sys


def setup_logging(
    level: str | None = None,
    format_string: str | None = None,
) -> None:
    """
    Setup logging configuration.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
               If None, reads from LOG_LEVEL environment variable
        format_string: Custom format string. If None, uses default format
    """
    # Get log level from parameter or environment
    log_level_str = level or os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Default format
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configure logging
    logging.basicConfig(
        level=log_level,
        format=format_string,
        stream=sys.stdout,
    )

    # Set log level for third-party libraries (optional)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
