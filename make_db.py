#!/usr/bin/env python3

import sqlite3

DB_FILE = "file_hashes.db"  # Your SQLite database file


def create_database():
    """
    This function creates the necessary tables in the SQLite database if they don't already exist.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # Table for storing file paths, content hashes, and modification times
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS file_hashes (
                    file_path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL,
                    mtime REAL NOT NULL
                )
            """
            )

            # Table for storing skipped files with the reason for skipping
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS skipped_files (
                    file_path TEXT PRIMARY KEY,
                    reason TEXT NOT NULL
                )
            """
            )

            # Table for logging all general events, errors, and other actions
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating database tables: {e}")
