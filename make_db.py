#!/usr/bin/env python3

import sqlite3
import logging

# Database file path
DB_FILE = 'file_hashes.db'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_database():
    try:
        # Create or connect to the database using a context manager
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # Log the database connection
            logging.info(f"Connected to the database at {DB_FILE}")

            # Table for storing file path, hash, and modification time
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_hashes (
                    file_path TEXT PRIMARY KEY,
                    hash TEXT NOT NULL,
                    mtime REAL NOT NULL
                )
            ''')
            logging.info("Created or verified the 'file_hashes' table.")

            # Table for storing skipped files or errors with reason
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS skipped_files (
                    file_path TEXT PRIMARY KEY,
                    reason TEXT NOT NULL
                )
            ''')
            logging.info("Created or verified the 'skipped_files' table.")

            # Commit changes (optional, since the `with` block will handle it)
            conn.commit()
            logging.info("Database schema is up-to-date and changes committed.")

    except sqlite3.Error as e:
        logging.error(f"An error occurred while working with SQLite: {e}")
    finally:
        logging.info("Database connection closed.")

if __name__ == "__main__":
    create_database()
