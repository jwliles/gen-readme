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


def scan_directory_with_parallelism(directory):
    """
    Scan the directory while excluding hidden files and certain folders.
    Uses multithreading to parallelize the scanning of files.
    """
    files_metadata = []
    all_files = []

    # Traverse the directory structure and collect all file paths
    for root, dirs, files in os.walk(directory):
        # Exclude hidden directories and specific excluded directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS]
        for file in files:
            if not file.startswith("."):  # Ignore hidden files
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    total_files = len(all_files)

    # Use ThreadPoolExecutor to process files in parallel
    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
        future_to_file = {
            executor.submit(process_file, file_path): file_path
            for file_path in all_files
        }

        with tqdm(total=total_files, desc="Scanning files") as pbar:
            for future in as_completed(future_to_file):
                result = future.result()
                if result:
                    files_metadata.append(result)
                pbar.update(1)

    return files_metadata
