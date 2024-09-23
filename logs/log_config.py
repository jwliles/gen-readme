#!/usr/bin/env python3

import logging


def configure_logging(log_level=logging.WARNING):
    """
    Configure the logging for the application.
    :param log_level: The logging level (default is INFO)
    """
    try:
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler()  # You can add more handlers here (e.g., FileHandler)
            ],
        )
        logging.info("Logging has been configured successfully.")
    except Exception as e:
        print(f"Failed to configure logging: {e}")
