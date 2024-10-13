#!/usr/bin/env python3

import argparse
import os
import json
import logging
import sqlite3
from logger import log_event, report_skipped_files
from readme_writer import write_readme
from file_scanner import scan_directory_with_parallelism
from make_db import DB_FILE, create_database
from metrics import ScanMetrics
from change_detector import detect_changes

print(f"Database path being used: {DB_FILE}")


# Load settings from JSON
def load_settings():
    """Load the user settings from settings.json."""
    with open("settings.json", "r") as f:
        return json.load(f)


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
        # Log the directories being processed
        logging.info(f"Processing directory: {directory}")

        # List subdirectories and files
        subdirs = [
            d
            for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]
        files = [
            f
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]

        # Write the README
        date_str = datetime.now().strftime("%Y-%m-%d")
        write_readme(directory, files, subdirs, date_str)

        if changes:
            logging.info(f"Updated README for {directory}.")
            log_event("INFO", f"README updated for {directory}")
        else:
            logging.info(f"No changes detected for {directory}. README not updated.")

    except Exception as e:
        logging.error(f"Error in write_readme_files: {e}")
        log_event("ERROR", f"Error in write_readme_files: {e}")


# Main function to scan directory and collect statistics
def scan_directory_and_collect_stats(directory, depth):
    """Scan the directory and collect statistics for reporting."""
    metrics = ScanMetrics()  # Initialize the ScanMetrics object
    metrics.start_timer()  # Start the timer
    log_event("INFO", "Scan started")

    # Load hashes from the database
    stored_hashes = load_hashes_from_db(DB_FILE)

    # Perform the scan and detect changes
    changes, current_file_hashes = detect_changes(
        directory,
        stored_hashes,
        lambda d: scan_directory_with_parallelism(d, depth),
        DB_FILE,
    )

    # Track statistics
    for _ in current_file_hashes:
        metrics.increment_files_scanned()  # Increment total files scanned

    # Write README files and update statistics
    if changes:
        write_readme_files(directory, changes)  # Update the README
        for file in changes:
            if "README.md" in file:
                metrics.increment_readme_updated()

    metrics.stop_timer()  # Stop the timer
    metrics.display_metrics()  # Display statistics

    log_event("INFO", "Scan completed")


def main():
    settings = load_settings()
    default_folder = settings.get("default_folder")

    parser = argparse.ArgumentParser(
        description="Generate README files for a directory and its subdirectories."
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Root directory path. Defaults to the current working directory or a user-defined default folder.",
        default=None,
    )
    parser.add_argument(
        "-d",
        "--depth",
        help="Depth to scan into the directory structure. Defaults to unlimited depth.",
        type=int,
        default=-1,
    )

    args = parser.parse_args()

    # Determine the path
    if args.path is None:
        if default_folder:
            print(f"Using default folder: {default_folder}")
            root_path = default_folder
        else:
            root_path = os.getcwd()  # Fallback to current directory
    elif args.path == ".":
        root_path = os.getcwd()
    else:
        root_path = args.path

    # Ensure database is created and ready
    create_database()

    # Call the scanning function and collect statistics
    scan_directory_and_collect_stats(root_path, args.depth)

    # Report skipped files (if any)
    report_skipped_files(DB_FILE)


if __name__ == "__main__":
    main()
