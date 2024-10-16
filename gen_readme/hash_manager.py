#!/usr/bin/env python3

import hashlib
import sqlite3
from gen_readme.logger import (
    log_skipped_file,
    log_event,
)  # Import log_event for logging into the database

# Clear any existing logging handlers to prevent terminal output
import logging

logging.getLogger().handlers.clear()


def compute_file_hash(file_path, chunk_size=4096):
    """Compute the hash of a file by reading it in chunks."""
    hash_obj = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)
    except FileNotFoundError:
        log_event("ERROR", f"File not found: {file_path}")
        return None
    except OSError as e:
        log_event("ERROR", f"Error reading file {file_path}: {e}")
        return None
    return hash_obj.hexdigest()


def compute_content_hash(content):
    """Compute the hash of a list of content lines."""
    return hashlib.md5("".join(content).encode("utf-8")).hexdigest()


# This list will accumulate file data until it reaches the batch size
file_hashes_batch = []


def save_file_hash(db_file, file_path, file_hash, mtime, batch_size=1000):
    """Insert or update a file hash in the file_hashes table using batching."""
    global file_hashes_batch
    try:
        # Add the file hash information to the batch list
        file_hashes_batch.append((file_path, file_hash, mtime))

        # If the batch size is reached, perform a bulk insert/update
        if len(file_hashes_batch) >= batch_size:
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()

                # Use executemany for batch processing
                cursor.executemany(
                    """
                    INSERT OR REPLACE INTO file_hashes (file_path, hash, mtime)
                    VALUES (?, ?, ?)
                    """,
                    file_hashes_batch,
                )

                conn.commit()
                log_event("INFO", f"Batch of {len(file_hashes_batch)} hashes saved.")

            # Clear the batch after committing
            file_hashes_batch = []

    except sqlite3.Error as e:
        # Log the error using the log_event function
        error_message = f"Failed to save hash for {file_path}. Error: {e}"
        log_event("ERROR", error_message)

        # Correct usage of log_skipped_file with two arguments
        log_skipped_file(file_path, error_message)


def flush_file_hashes(db_file):
    """Flush any remaining file hashes in the batch."""
    global file_hashes_batch
    if file_hashes_batch:
        try:
            with sqlite3.connect(db_file) as conn:
                cursor = conn.cursor()

                # Use executemany for batch processing of the remaining hashes
                cursor.executemany(
                    """
                    INSERT OR REPLACE INTO file_hashes (file_path, hash, mtime)
                    VALUES (?, ?, ?)
                    """,
                    file_hashes_batch,
                )

                conn.commit()
                log_event(
                    "INFO", f"Final batch of {len(file_hashes_batch)} hashes saved."
                )

            # Clear the batch after committing
            file_hashes_batch = []

        except sqlite3.Error as e:
            error_message = f"Failed to flush remaining hashes. Error: {e}"
            log_event("ERROR", error_message)
            for file_path, _, _ in file_hashes_batch:
                log_skipped_file(file_path, error_message)
