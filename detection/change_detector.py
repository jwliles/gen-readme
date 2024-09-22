#!/usr/bin/env python3

from hashing.hash_computer import compute_file_hash


def detect_changes(directory, stored_hashes, scan_directory_func):
    """Detect changes in the directory by comparing file hashes."""
    changes = []
    current_file_hashes = {}

    # Scan the directory and compute hashes
    files_metadata = scan_directory_func(directory)
    for file_path, mtime in files_metadata:
        file_hash = compute_file_hash(file_path)
        if file_hash is None:
            continue

        current_file_hashes[file_path] = file_hash

        # Check if the file hash has changed
        if stored_hashes.get(file_path) != file_hash:
            changes.append(file_path)

    return changes, current_file_hashes
