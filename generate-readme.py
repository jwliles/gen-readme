#!/usr/bin/env python3

import argparse
import logging
import os
import sqlite3
from logger import log_event, report_skipped_files
from datetime import datetime
from readme_writer import write_readme
from file_scanner import scan_directory_with_parallelism
from hash_manager import load_hashes_from_db
from make_db import DB_FILE, create_database
from metrics import ScanMetrics
from change_detector import detect_changes  # Importing detect_changes from your new module

print(f"Database path being used: {DB_FILE}")


def load_hashes_from_db(db_file):
    """Load hashes from the database."""
    hashes = {}
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path, hash FROM file_hashes")
            for row in cursor.fetchall():
                hashes[row[0]] = row[1]
    except sqlite3.Error as e:
        logging.error(f"Failed to load hashes from database: {e}")
        log_event("ERROR", f"Failed to load hashes from database: {e}")
    return hashes


def write_readme_files(directory, changes):
    """Write README.md files for the directory and its subdirectories."""
    try:
        # List subdirectories and files
        subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        # Write the README
        date_str = datetime.now().strftime("%Y-%m-%d")
        write_readme(directory, files, subdirs, date_str)

        if changes:
            logging.info(f"Updated README for {directory}.")
            log_event("INFO", f"README updated for {directory}")

    except Exception as e:
        logging.error(f"Error in write_readme_files: {e}")
        log_event("ERROR", f"Error in write_readme_files: {e}")


def scan_directory_and_collect_stats(directory):
    """Scan the directory and collect statistics for reporting."""
    metrics = ScanMetrics()  # Initialize the ScanMetrics object
    metrics.start_timer()  # Start the timer
    log_event("INFO", "Scan started")

    # Load hashes from the database
    stored_hashes = load_hashes_from_db(DB_FILE)

    # Perform the scan and detect changes
    changes, current_file_hashes = detect_changes(directory, stored_hashes, scan_directory_with_parallelism, DB_FILE)

    # Track statistics
    for _ in current_file_hashes:
        metrics.increment_files_scanned()  # Increment total files scanned

    # Write README files and update statistics
    if changes:
        write_readme_files(directory, changes)  # Update the README
        for file in changes:
            if "README.md" in file:
                metrics.increment_readme_updated()

    # Simulate skipped files count (this should be replaced with actual logic)
    metrics.skipped_files_count = 5  # Replace with actual skipped files logic

    metrics.stop_timer()  # Stop the timer
    metrics.display_metrics()  # Display statistics

    log_event("INFO", "Scan completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate README files for a directory and its subdirectories.")
    parser.add_argument("-p", "--path", help="Root directory path. Defaults to the current working directory.",
                        default=os.getcwd())
    args = parser.parse_args()

    root_path = args.path

    # Ensure database is created and ready
    create_database()

    # Call the scanning function and collect statistics
    scan_directory_and_collect_stats(root_path)

    # Report skipped files (if any)
    report_skipped_files(DB_FILE)
