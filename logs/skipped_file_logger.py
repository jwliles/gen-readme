#!/usr/bin/env python3

import logging


def log_skipped_file(file_path, reason):
    """Log skipped file and the reason."""
    logging.info(f"Skipped: {file_path}, Reason: {reason}")
