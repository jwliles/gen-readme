#!/usr/bin/env python3

import os
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


if __name__ == "__main__":
    main()
