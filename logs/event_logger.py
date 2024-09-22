#!/usr/bin/env python3

import logging


def log_event(level, message):
    """Log an event with the given level and message."""

    # Convert string level to logging level constant
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # Ensure the level is converted to an integer
    log_level = log_levels.get(
        level, logging.INFO
    )  # Default to INFO if the level is unknown

    # Log the event with the appropriate level
    logging.log(log_level, message)
