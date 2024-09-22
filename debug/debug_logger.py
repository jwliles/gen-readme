#!/usr/bin/env python3

import logging


def configure_debug_logging():
    """Configure logging for detailed debugging."""
    logging.basicConfig(
        level=logging.DEBUG,  # Change to INFO or WARNING for less verbosity
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("debug_log.log"),  # Logs will be saved here
            logging.StreamHandler(),  # Also prints to the terminal
        ],
    )
    logging.info("Debug logging configured successfully.")
