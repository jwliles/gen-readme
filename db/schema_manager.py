#!/usr/bin/env python3

import sqlite3
import logging

DB_FILE = "file_hashes.db"


def create_database():
    """Create the database schema for storing file hashes."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS file_hashes (
                    file_path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL,
                    mtime REAL NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS skipped_files (
                    file_path TEXT PRIMARY KEY,
                    reason TEXT
                )
            """
            )
            conn.commit()
            logging.info(f"Database created/verified at {DB_FILE}")
    except sqlite3.Error as e:
        logging.error(f"Database creation error: {e}")
