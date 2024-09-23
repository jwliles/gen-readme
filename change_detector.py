# change_detector.py

import logging
from hash_manager import compute_file_hash, save_file_hash
from logger import log_skipped_file, log_event


def detect_changes(directory, stored_hashes, scan_directory_with_parallelism, DB_FILE):
    """Detect changes in the directory by comparing file hashes."""
    changes = []
    current_file_hashes = {}

    # Scan the directory and get metadata for all files (file paths and modification times)
    files_metadata = scan_directory_with_parallelism(directory)

    # Initialize a counter to keep track of processed files
    files_processed = 0
    total_files = len(files_metadata)

    print(f"Starting scan: {total_files} files to process...")

    for file_path, mtime in files_metadata:
        file_hash = compute_file_hash(file_path)
        if file_hash is None:
            logging.error(f"Hash for {file_path} could not be computed")
            log_skipped_file(
                file_path, "Hash could not be computed"
            )  # Log skipped files
            files_processed += 1
            continue

        if file_hash:
            current_file_hashes[file_path] = file_hash

            # Check if the file hash has changed
            if stored_hashes.get(file_path) != file_hash:
                changes.append(file_path)

            # Save file hash to the database
            try:
                save_file_hash(DB_FILE, file_path, file_hash, mtime)
            except Exception as e:
                logging.error(f"Failed to save hash for {file_path}: {e}")
                log_event("ERROR", f"Failed to save hash for {file_path}: {e}")

        # Increment the counter
        files_processed += 1

        # Print the current progress every 100 files (or adjust as necessary)
        if files_processed % 100 == 0 or files_processed == total_files:
            print(f"Processed {files_processed}/{total_files} files")

    return changes, current_file_hashes
