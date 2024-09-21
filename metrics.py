#!/usr/bin/env python3

import time
from logger import log_event  # Import logging to store metrics in the database


class ScanMetrics:
    """Class to track and display scan metrics."""

    def __init__(self):
        # Initialize counters
        self.total_files_scanned = 0
        self.skipped_files_count = 0
        self.readme_files_created = 0
        self.readme_files_updated = 0
        self.start_time = None
        self.end_time = None

    def start_timer(self):
        """Start the timer for the scan."""
        self.start_time = time.time()

    def stop_timer(self):
        """Stop the timer for the scan."""
        self.end_time = time.time()

    def get_duration(self):
        """Return the duration of the scan."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0

    def get_average_scan_rate(self):
        """Return the average number of files scanned per second."""
        duration = self.get_duration()
        return self.total_files_scanned / duration if duration > 0 else 0

    def display_metrics(self):
        """Display the scan metrics in the terminal."""
        duration = self.get_duration()
        avg_scan_rate = self.get_average_scan_rate()

        print("\nScan Statistics:")
        print(f"Total files scanned: {self.total_files_scanned}")
        print(f"Skipped files: {self.skipped_files_count}")
        print(f"README files created: {self.readme_files_created}")
        print(f"README files updated: {self.readme_files_updated}")
        print(f"Total time taken: {duration:.2f} seconds")
        print(f"Average scan rate: {avg_scan_rate:.2f} files/second")

        # Optionally log the statistics to the database
        log_event("INFO",
                  f"Scan completed. Total files: {self.total_files_scanned}, Skipped: {self.skipped_files_count}, Created: {self.readme_files_created}, Updated: {self.readme_files_updated}, Time: {duration:.2f} sec, Rate: {avg_scan_rate:.2f} files/sec")

    def increment_files_scanned(self):
        """Increment the total files scanned counter."""
        self.total_files_scanned += 1

    def increment_skipped_files(self):
        """Increment the skipped files counter."""
        self.skipped_files_count += 1

    def increment_readme_created(self):
        """Increment the README files created counter."""
        self.readme_files_created += 1

    def increment_readme_updated(self):
        """Increment the README files updated counter."""
        self.readme_files_updated += 1
