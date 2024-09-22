#!/usr/bin/env python3

import time


class ScanMetrics:
    def __init__(self):
        self.files_scanned = 0
        self.start_time = 0
        self.end_time = 0

    def increment_files_scanned(self):
        self.files_scanned += 1

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.end_time = time.time()

    def display_metrics(self):
        total_time = self.end_time - self.start_time
        print(f"Total files scanned: {self.files_scanned}")
        print(f"Total time taken: {total_time:.2f} seconds")
