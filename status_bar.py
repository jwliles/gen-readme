#!/usr/bin/env python3

from tqdm import tqdm
import os

def scan_directory_with_progress(directory):
    """
    Scan the directory and return file paths and metadata.
    A progress bar is used to display the current state of the scan.
    """
    files_metadata = []

    # Traverse the directory structure and count total files
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    with tqdm(total=total_files, desc="Scanning files") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                if not file.startswith('.'):  # Ignore hidden files
                    file_path = os.path.join(root, file)
                    mtime = os.path.getmtime(file_path)
                    files_metadata.append((file_path, mtime))
                    pbar.update(1)

    return files_metadata

# The function `scan_directory_with_progress` will be used in the main script to show progress during the directory scan.
# The rest of the scanning logic remains the same, but now includes a progress bar for better visibility.

