#!/usr/bin/env python3

import hashlib
import sqlite3
import logging
from logger import log_skipped_file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def compute_file_hash(file_path, chunk_size=4096):
    """Compute the hash of a file by reading it in chunks."""
    hash_obj = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                hash_obj.update(chunk)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except OSError as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None
    return hash_obj.hexdigest()


def compute_content_hash(content):
    """Compute the hash of a list of content lines."""
    return hashlib.md5("".join(content).encode("utf-8")).hexdigest()


def save_file_hash(db_file, file_path, file_hash, mtime):
    """Insert or update a file hash in the file_hashes table."""
    try:
        # Use context manager for the SQLite connection
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()

            # Insert or update the file hash in the database
            cursor.execute('''
                INSERT OR REPLACE INTO file_hashes (file_path, hash, mtime)
                VALUES (?, ?, ?)
            ''', (file_path, file_hash, mtime))

            conn.commit()
            logging.info(f"Hash saved for {file_path}: {file_hash}")

    except sqlite3.Error as e:
        # Log and handle the error using the log_skipped_file function
        error_message = f"Failed to save hash for {file_path}. Error: {e}"
        logging.error(error_message)
        log_skipped_file(db_file, file_path, error_message)
