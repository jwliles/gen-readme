#!/usr/bin/env python3
import sys


class TerminalOutput:

    @staticmethod
    def update_progress(current, total):
        """Display the current progress in the terminal."""
        sys.stdout.write(f"\rProcessed {current}/{total} files")
        sys.stdout.flush()

        # Ensure progress display completes with a newline when done
        if current == total:
            sys.stdout.write("\n")

    @staticmethod
    def display_metrics(total_files, time_taken, avg_rate):
        """Print scan metrics in the terminal."""
        print(f"\nTotal files scanned: {total_files}")
        print(f"Total time taken: {time_taken:.2f} seconds")
        print(f"Average scan rate: {avg_rate:.2f} files/second")

    @staticmethod
    def print_message(message, level="INFO"):
        """Generic method to print messages with levels."""
        print(f"{level}: {message}")


def display_scan_statistics(
    metrics, skipped_files, readmes_created, readmes_updated, total_files, total_time
):
    """Display the scan statistics in the terminal."""
    print("\nScan Statistics:")
    print(f"Total files scanned: {metrics.files_scanned}")
    print(f"Skipped files: {skipped_files}")
    print(f"README files created: {readmes_created}")
    print(f"README files updated: {readmes_updated}")
    print(f"Total time taken: {total_time:.2f} seconds")
    print(f"Average scan rate: {metrics.files_scanned / total_time:.2f} files/second")


def display_progress(current, total):
    """Display the progress of the scan."""
    print(f"\rProcessed {current}/{total} files", end="")
