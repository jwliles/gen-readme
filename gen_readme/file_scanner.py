#!/usr/bin/env python3

import logging
import os
import fnmatch
import argparse
import json
from concurrent.futures import ThreadPoolExecutor

# Path to the settings file
SETTINGS_FILE = os.path.expanduser("~/.gen_readme/settings.json")


# Load settings, including EXCLUDED_DIRS, from the settings file
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
        return settings
    except FileNotFoundError:
        # If the settings file doesn't exist, return default settings
        return {"EXCLUDED_DIRS": [".git", ".config", "venv"]}


# Save settings to the settings file
def save_settings(settings):
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


# Check if a directory path matches any pattern in EXCLUDED_DIRS
def is_excluded_dir(path, excluded_patterns):
    for pattern in excluded_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def process_file(file_path):
    """
    Process an individual file: get its metadata (e.g., modification time).
    """
    try:
        mtime = os.path.getmtime(file_path)
        return file_path, mtime
    except OSError:
        return None


def get_file_metadata(file_path):
    """Get metadata for a single file."""
    try:
        mtime = os.path.getmtime(file_path)
        return file_path, mtime
    except OSError as e:
        logging.error(f"Error getting metadata for {file_path}: {e}")
        return None


def scan_directory_with_parallelism(directory, max_workers=4):
    """Scan the directory and return metadata using parallel workers."""
    settings = load_settings()
    excluded_dirs = settings.get("EXCLUDED_DIRS", [])

    files_metadata = []
    all_files = []

    for root, dirs, files in os.walk(directory):
        # Filter out excluded directories
        dirs[:] = [
            d for d in dirs if not is_excluded_dir(os.path.join(root, d), excluded_dirs)
        ]
        for file in files:
            all_files.append(os.path.join(root, file))

    # Use ThreadPoolExecutor to parallelize file scanning
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(get_file_metadata, file) for file in all_files]
        for future in futures:
            try:
                result = future.result()
                if result:
                    files_metadata.append(result)
            except Exception as e:
                logging.error(f"Error scanning file: {e}")

    return files_metadata


def manage_excluded_dirs(action, pattern=None, old_pattern=None):
    settings = load_settings()
    excluded_dirs = settings.get("EXCLUDED_DIRS", [])

    if action == "add" and pattern:
        if pattern not in excluded_dirs:
            excluded_dirs.append(pattern)
            print(f"Added '{pattern}' to excluded directories.")
        else:
            print(f"'{pattern}' is already in the list of excluded directories.")

    elif action == "remove" and pattern:
        if pattern in excluded_dirs:
            excluded_dirs.remove(pattern)
            print(f"Removed '{pattern}' from excluded directories.")
        else:
            print(f"'{pattern}' not found in the list of excluded directories.")

    elif action == "modify" and pattern and old_pattern:
        if old_pattern in excluded_dirs:
            excluded_dirs[excluded_dirs.index(old_pattern)] = pattern
            print(f"Modified '{old_pattern}' to '{pattern}'.")
        else:
            print(f"'{old_pattern}' not found in the list of excluded directories.")

    elif action == "list":
        print("Current excluded directories/patterns:")
        for d in excluded_dirs:
            print(f" - {d}")

    settings["EXCLUDED_DIRS"] = excluded_dirs
    save_settings(settings)


def main():
    parser = argparse.ArgumentParser(
        description="File Scanner with Directory Exclusion Management"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Add command
    add_parser = subparsers.add_parser(
        "add", help="Add a directory pattern to EXCLUDED_DIRS"
    )
    add_parser.add_argument("pattern", type=str, help="Pattern to add (e.g., */tmp)")

    # Remove command
    remove_parser = subparsers.add_parser(
        "remove", help="Remove a directory pattern from EXCLUDED_DIRS"
    )
    remove_parser.add_argument("pattern", type=str, help="Pattern to remove")

    # Modify command
    modify_parser = subparsers.add_parser(
        "modify", help="Modify an existing directory pattern"
    )
    modify_parser.add_argument("old_pattern", type=str, help="Old pattern to replace")
    modify_parser.add_argument("new_pattern", type=str, help="New pattern")

    # List command
    list_parser = subparsers.add_parser(
        "list", help="List all patterns in EXCLUDED_DIRS"
    )

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan a directory")
    scan_parser.add_argument("directory", type=str, help="Directory to scan")
    scan_parser.add_argument(
        "--workers", type=int, default=4, help="Number of workers for parallel scanning"
    )

    args = parser.parse_args()

    if args.command == "add":
        manage_excluded_dirs("add", args.pattern)
    elif args.command == "remove":
        manage_excluded_dirs("remove", args.pattern)
    elif args.command == "modify":
        manage_excluded_dirs("modify", args.new_pattern, args.old_pattern)
    elif args.command == "list":
        manage_excluded_dirs("list")
    elif args.command == "scan":
        metadata = scan_directory_with_parallelism(args.directory, args.workers)
        print(f"Scanned {len(metadata)} files.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
