#!/usr/bin/env python3

import os
import concurrent.futures
import time


def get_file_metadata(file_path):
    """Return the file path and modification time for a file."""
    try:
        mtime = os.path.getmtime(file_path)
        return file_path, mtime
    except OSError:
        return None


def scan_directory_with_parallelism(directory, max_workers=None):
    """Scan files in the directory using parallel processing."""
    files_metadata = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for root, dirnames, files in os.walk(directory):
            # Skip hidden directories and files
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            files = [f for f in files if not f.startswith(".")]

            # Submit batches of files for parallel scanning
            futures += [
                executor.submit(get_file_metadata, os.path.join(root, file))
                for file in files
            ]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                files_metadata.append(result)

    return files_metadata
