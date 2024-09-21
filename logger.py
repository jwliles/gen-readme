#!/usr/bin/env python3

import logging
import sqlite3
from logging.handlers import RotatingFileHandler

DB_FILE = 'file_hashes.db'  # Your SQLite database file

def setup_logging(log_file="script.log"):
    """
    Set up logging to write ONLY to a log file and completely suppress terminal output.
    """
    # Define a custom logging format
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    # Set up the root logger to handle log file output
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Log all levels to the file

    # File handler for logging everything into a file
    log_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=5)
    log_handler.setLevel(logging.DEBUG)  # Log everything to the file
    log_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(log_handler)

    # Ensure no logging is sent to the terminal
    root_logger.handlers = [log_handler]  # Only log to file, not terminal

def log_event(event_type, message):
    """
    Log an event into the 'events' table in the SQLite database.
    This can be used for any type of logging such as errors, general actions, etc.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO events (event_type, message) VALUES (?, ?)', (event_type, message))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error logging event: {e}")


def log_file_hash(file_path, file_hash, mtime):
    """
    Log file hash and metadata into the SQLite database.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR REPLACE INTO file_hashes (file_path, hash, mtime) VALUES (?, ?, ?)', (file_path, file_hash, mtime))
            conn.commit()
    except sqlite3.Error as e:
        log_event("ERROR", f"Failed to log file hash for {file_path}. Reason: {e}")


def report_skipped_files(db_file):
    """
    Log the skipped files from the database into the log file.
    """
    try:
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path, reason FROM skipped_files")
            skipped_files = cursor.fetchall()

        if skipped_files:
            for file_path, reason in skipped_files:
                logging.info(f"Skipped: {file_path}, Reason: {reason}")

    except sqlite3.Error as e:
        logging.error(f"Failed to retrieve skipped files. Error: {e}")


def log_skipped_file(file_path, reason):
    """
    Log skipped files into the SQLite database.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO skipped_files (file_path, reason) VALUES (?, ?)', (file_path, reason))
            conn.commit()
    except sqlite3.Error as e:
        log_event("ERROR", f"Failed to log skipped file {file_path}. Reason: {e}")