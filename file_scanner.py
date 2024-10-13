#!/usr/bin/env python3

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

EXCLUDED_DIRS = {".git", ".config", "venv"}  # Add other folders to exclude here


def process_file(file_path):
    """
    Process an individual file: get its metadata (e.g., modification time).
    """
    try:
        mtime = os.path.getmtime(file_path)
        return file_path, mtime
    except OSError:
        return None


def scan_directory_with_parallelism(directory, max_depth=-1):
    """
    Scan the directory while excluding hidden files and certain folders.
    Uses multithreading to parallelize the scanning of files.
    max_depth: If specified, limits the depth of directory scanning.
    """
    files_metadata = []
    all_files = []

    def should_scan_directory(current_depth):
        return max_depth == -1 or current_depth <= max_depth

    # Traverse the directory structure and collect all file paths
    for root, dirs, files in os.walk(directory):
        depth = root[len(directory) :].count(os.sep)

        if not should_scan_directory(depth):
            continue

        # Exclude hidden directories and specific excluded directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS]
        for file in files:
            if not file.startswith("."):  # Ignore hidden files
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    total_files = len(all_files)

    # Use ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_file = {
            executor.submit(process_file, file_path): file_path
            for file_path in all_files
        }

        for future in as_completed(future_to_file):
            result = future.result()
            if result:
                files_metadata.append(result)

    return files_metadata
