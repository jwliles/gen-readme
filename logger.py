#!/usr/bin/env python3

import json
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file="script.log"):
    """
    Set up logging configuration.
    Logs everything to a file, no terminal output.
    Logs are in structured JSON format for better parsing and sorting.
    """

    # Define a custom logging format with JSON structure
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "time": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "filename": record.filename,
                "funcName": record.funcName,
                "lineno": record.lineno
            }
            return json.dumps(log_record)

    # Set up logging to file with rotation (to avoid growing log files indefinitely)
    log_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)  # 5MB log size before rotating
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(JsonFormatter())

    # Get root logger and remove any default handlers
    root_logger = logging.getLogger()
    root_logger.handlers = []  # Remove other handlers (like StreamHandler)

    # Add our custom file handler
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(log_handler)

    logging.debug("Logging setup complete - all logs going to file, none to terminal.")


# Example log functions, similar to the original ones but simplified for demonstration

def log_skipped_file(db_file, file_path, reason):
    """
    Log skipped files or errors into a database and as a structured log.
    """
    try:
        # Example: In a real case, log details would be stored in a database
        logging.info(f"Skipped file: {file_path}, Reason: {reason}")
    except Exception as e:
        logging.error(f"Failed to log skipped file: {file_path}, Error: {e}")


def report_skipped_files():
    """
    Placeholder function to demonstrate logging when skipped files are reported.
    """
    try:
        # Example: Fetching from a database would happen here
        logging.info("Report: All skipped files have been processed.")
    except Exception as e:
        logging.error(f"Failed to report skipped files: {e}")


# After modifying, this will be the main logger setup in the updated file.
setup_logging()
