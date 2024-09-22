#!/usr/bin/env python3

from metrics.scan_metrics import ScanMetrics
from detection.change_detector import detect_changes
from db.hash_db import load_hashes_from_db
from output.readme_manager import create_or_update_readme
from .file_scanner import scan_directory_with_parallelism
from output.terminal_output import TerminalOutput
import os


def should_skip_file(file_path):
    """Skip files that are hidden (starting with a dot)."""
    return os.path.basename(file_path).startswith(".")


def scan_directory_and_collect_stats(directory):
    """Scan the directory and collect statistics for reporting."""
    metrics = ScanMetrics()
    metrics.start_timer()

    # Load file hashes from the database
    stored_hashes = load_hashes_from_db("file_hashes.db")

    # Detect changes in the directory
    changes, current_file_hashes = detect_changes(
        directory, stored_hashes, scan_directory_with_parallelism
    )

    # Track metrics
    total_files = len(current_file_hashes)
    readmes_created = 0
    readmes_updated = 0
    skipped_files = 0

    for idx, file_path in enumerate(current_file_hashes, start=1):
        metrics.increment_files_scanned()

        # Skip hidden files or directories
        if should_skip_file(file_path):
            skipped_files += 1
            continue

        # Get subdirectories and files for the current directory
        dirpath, dirnames, filenames = next(os.walk(directory))

        subdirs = dirnames
        files = filenames

        # Write README files if changes are detected
        if changes:
            if create_or_update_readme(dirpath, files, subdirs, changes):
                readmes_created += 1
            else:
                readmes_updated += 1

        # Update progress in the terminal every 10 files
        if idx % 10 == 0 or idx == total_files:
            TerminalOutput.update_progress(idx, total_files)

    # Stop the timer and return relevant stats
    metrics.stop_timer()
    return (
        metrics,
        total_files,
        skipped_files,
        readmes_created,
        readmes_updated,
        changes,
    )
