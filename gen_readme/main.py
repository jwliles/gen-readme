#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sqlite3

from gen_readme.change_detector import detect_changes
from gen_readme.file_scanner import scan_directory_with_parallelism
from gen_readme.logger import log_event, report_skipped_files
from gen_readme.make_db import DB_FILE, create_database
from gen_readme.metrics import ScanMetrics
from gen_readme.readme_generator import (
    generate_all_readme_files,
)  # Now importing from the renamed module

print(f"Database path being used: {DB_FILE}")


# Load settings from JSON
def load_settings():
    """Load the user settings from settings.json."""
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Settings file not found.")
        return {}


# Load hashes from the database
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


# Main function to scan directory and collect statistics
def scan_directory_and_collect_stats(directory, depth):
    """Scan the directory and collect statistics for reporting."""
    metrics = ScanMetrics()
    metrics.start_timer()
    log_event("INFO", "Scan started")

    stored_hashes = load_hashes_from_db(DB_FILE)

    # Perform the scan and detect changes
    changes, current_file_hashes = detect_changes(
        directory,
        stored_hashes,
        lambda d: scan_directory_with_parallelism(
            d, max_workers=4
        ),  # Set max_workers properly
        DB_FILE,
    )

    # Track statistics
    for _ in current_file_hashes:
        metrics.increment_files_scanned()

    generate_all_readme_files(directory, changes, metrics, use_template=False)

    metrics.stop_timer()
    metrics.display_metrics()
    log_event("INFO", "Scan completed")


def main():
    parser = argparse.ArgumentParser(
        description="Generate README files for a directory and its subdirectories.",
        epilog="Example usage: gen_readme -p /mydir -d 2 -v",
    )
    parser.add_argument(
        "-p",
        "--path",
        help="Root directory path. Defaults to the current working directory.",
        default=os.getcwd(),
        metavar="DIR",
    )
    parser.add_argument(
        "-d",
        "--depth",
        help="Depth to scan into the directory structure. Defaults to unlimited depth.",
        type=int,
        default=-1,
        metavar="N",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Enable verbose output for debugging.",
        action="store_true",
    )

    args = parser.parse_args()

    # Configure logging level based on verbose flag
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    # Set the root path and ensure the database is created
    root_path = args.path
    create_database()

    # Call the scanning function and collect statistics
    scan_directory_and_collect_stats(root_path, args.depth)

    # Report any skipped files
    report_skipped_files(DB_FILE)


if __name__ == "__main__":
    import cProfile, pstats

    #    profiler = cProfile.Profile()
    #    profiler.enable()
    main()
#    profiler.disable()
#    stats = pstats.Stats(profiler).sort_stats("tottime")
#    stats.print_stats()
