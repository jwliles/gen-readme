#!/usr/bin/env python3
import logging
import os

from db.hash_db import load_hashes_from_db
from debug_logger import configure_debug_logging
from detection.change_detector import detect_changes
from scanning.scan_manager import scan_directory_and_collect_stats, should_skip_file
from scanning.file_scanner import scan_directory_with_parallelism


def run_test_scan(directory):
    """Run a test scan with detailed logging to identify issues."""
    # Start logging
    configure_debug_logging()

    logging.debug(f"Starting test scan for directory: {directory}")

    # Load file hashes
    try:
        stored_hashes = load_hashes_from_db("file_hashes.db")
        logging.debug(f"Loaded hashes: {len(stored_hashes)} hashes found.")
    except Exception as e:
        logging.error(f"Error loading hashes: {e}")

    # Start scanning directory
    try:
        changes, current_file_hashes = detect_changes(
            directory, stored_hashes, scan_directory_with_parallelism
        )
        logging.debug(f"Detected {len(current_file_hashes)} files in directory.")
        logging.debug(f"Detected {len(changes)} changes.")
    except Exception as e:
        logging.error(f"Error scanning directory: {e}")
        return

    # Log file processing
    for file_path in current_file_hashes:
        logging.debug(f"Processing file: {file_path}")
        if should_skip_file(file_path):
            logging.debug(f"Skipped file: {file_path}")
        else:
            logging.debug(f"Processing README for file: {file_path}")
            # Call to README creation or update here

    logging.debug(f"Test scan completed.")
