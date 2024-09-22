#!/usr/bin/env python3

import sqlite3
import logging


def save_file_hash(db_file, file_path, file_hash, mtime):
    """Save a file hash in the database."""
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO file_hashes (file_path, hash, mtime)
                VALUES (?, ?, ?)""",
                (file_path, file_hash, mtime),
            )
            conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Failed to save hash for {file_path}: {e}")


def load_hashes_from_db(db_file):
    """Load file hashes from the database."""
    hashes = {}
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path, hash FROM file_hashes")
            for row in cursor.fetchall():
                hashes[row[0]] = row[1]
    except sqlite3.Error as e:
        logging.error(f"Failed to load hashes from the database: {e}")
    return hashes
