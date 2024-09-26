#!/usr/bin/env python3

import argparse
import logging
import os
<<<<<<< HEAD
import argparse
import time
from logs.event_logger import log_event
from db.schema_manager import create_database
from logs.log_config import configure_logging
from output.terminal_output import display_scan_statistics
from scanning.scan_manager import scan_directory_and_collect_stats


def main():
    """Main function to parse arguments and initiate the scan."""
    parser = argparse.ArgumentParser(
        description="Generate README files for a directory and its subdirectories."
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Root directory path. Defaults to the current working directory.",
        default=os.getcwd(),
    )
    args = parser.parse_args()
    root_path = args.path

    # Initialize logging configuration
    configure_logging()

    # Display the database path being used
    db_path = "file_hashes.db"
    print(f"Database path being used: {db_path}")

    # Start the timer to track overall execution time
    overall_start_time = time.time()

    # Create or verify the database schema
    create_database()

    # Start the scan
    metrics, total_files, skipped_files, readmes_created, readmes_updated, changes = (
        scan_directory_and_collect_stats(root_path)
    )

    # Stop the overall execution timer
    overall_end_time = time.time()
    total_time = overall_end_time - overall_start_time

    # Display the scan statistics
    display_scan_statistics(
        metrics,
        skipped_files,
        readmes_created,
        readmes_updated,
        total_files,
        total_time,
    )

    # Log the completion of the scan
    log_event("INFO", "Scan completed")

    # Display the terminal execution time
    print(f"\nThe terminal reports an execution time of {total_time:.3f} seconds.")


=======
import sqlite3

# Import necessary modules
from datetime import datetime
from readme_writer import write_readme

# Importing from refactored modules
from file_scanner import scan_directory
from hash_manager import compute_file_hash, save_file_hash
from logger import log_skipped_file, report_skipped_files
from make_db import DB_FILE, create_database

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
    return hashes


def remove_last_update_line(content):
    """Remove the line containing the 'Last update' information."""
    return [line for line in content if not line.startswith(">There are")]


def detect_changes(directory, stored_hashes):
    """Detect changes in the directory by comparing file hashes."""
    changes = []
    current_file_hashes = {}

    # Scan the directory and compute hashes
    files_metadata = scan_directory(directory)
    for file_path, mtime in files_metadata:
        file_hash = compute_file_hash(file_path)
        if file_hash is None:
            logging.error(f"Hash for {file_path} could not be computed")
            continue

        if file_hash:
            current_file_hashes[file_path] = file_hash

            # Check if the file hash has changed
            if stored_hashes.get(file_path) != file_hash:
                changes.append(file_path)

            # Save file hash to the database
            try:
                logging.info(f"Attempting to save hash for {file_path} with hash {file_hash} and mtime {mtime}")
                save_file_hash(DB_FILE, file_path, file_hash, mtime)
                logging.info(f"Successfully saved hash for {file_path}")
            except Exception as e:
                logging.error(f"Failed to save hash for {file_path}: {e}")

    return changes, current_file_hashes


def write_readme_files(directory):
    """Write README.md files for the directory and its subdirectories."""
    try:
        old_file_hashes = load_hashes_from_db(DB_FILE)
        changes, current_file_hashes = detect_changes(directory, old_file_hashes)

        if changes:
            logging.info(f"Detected changes in {len(changes)} files.")

            # List subdirectories and files
            subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

            # Write the README
            date_str = datetime.now().strftime("%Y-%m-%d")
            write_readme(directory, files, subdirs, date_str)

            # Save updated hashes
            # No need to save hashes separately, they are already stored in the database
        else:
            logging.info(f"No changes detected for {directory}.")

    except Exception as e:
        logging.error(f"Error in write_readme_files: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate README files for a directory and its subdirectories.")
    parser.add_argument("-p", "--path", help="Root directory path. Defaults to the current working directory.",
                        default=os.getcwd())
    args = parser.parse_args()

    root_path = args.path

    try:
        # Create or update the hash database (if relevant)
        create_database()
        logging.info(f"Database created/verified at {DB_FILE}")

        # Add a test entry to the skipped_files table
        log_skipped_file(DB_FILE, "test_file.txt", "Test reason for skipping")

        # Continue with the rest of your script...
        write_readme_files(root_path)

        # Ensure skipped files are written to a log file
        report_skipped_files(DB_FILE, root_path)

    except Exception as e:
        logging.error(f"Error in main execution: {e}")


>>>>>>> 091ee6e (chore(files): Update files)
if __name__ == "__main__":
    main()
