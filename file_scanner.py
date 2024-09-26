#!/usr/bin/env python3

import os
from tqdm import tqdm

def scan_directory(directory):
    """Scan the directory and return file paths and metadata."""
    files_metadata = []

    # Traverse the directory structure
    total_files = sum([len(files) for _, _, files in os.walk(directory)])
    with tqdm(total=total_files, desc="Scanning files") as pbar:
        for root, _, files in os.walk(directory):
            for file in files:
                if not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    mtime = os.path.getmtime(file_path)
                    files_metadata.append((file_path, mtime))
                    pbar.update(1)

    return files_metadata

def get_file_metadata(file_path):
    """Get file metadata like mtime for a specific file."""
    try:
        mtime = os.path.getmtime(file_path)
        return {'path': file_path, 'mtime': mtime}
    except OSError:
        return None
