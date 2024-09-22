#!/usr/bin/env python3

import os
import concurrent.futures


def get_file_metadata(file_path):
    """Return the file path and modification time for a file."""
    try:
        mtime = os.path.getmtime(file_path)
        return file_path, mtime
    except OSError:
        return None


def scan_directory_with_parallelism(directory):
    """Scan files in the directory using parallel processing, skipping hidden files and directories."""
    files_metadata = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for root, dirnames, files in os.walk(directory):
            # Skip hidden directories and files
            dirnames[:] = [
                d for d in dirnames if not d.startswith(".")
            ]  # Skip hidden directories
            files = [f for f in files if not f.startswith(".")]  # Skip hidden files

            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(get_file_metadata, file_path))

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                files_metadata.append(result)

    return files_metadata
