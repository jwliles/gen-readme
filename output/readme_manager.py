#!/usr/bin/env python3

import os
from logs.event_logger import log_event


def create_or_update_readme(directory, files, subdirs, changes):
    """
    Create or update the README.md file in the specified directory with information on files and subdirectories.
    Return True if the README is newly created, False if it is updated.
    """
    readme_path = os.path.join(directory, "README.md")
    if not os.path.exists(readme_path):
        # Create README.md
        with open(readme_path, "w") as f:
            f.write("# Directory Listing\n\n")
            f.write(f"Directory: {directory}\n\n")
            f.write("## Files:\n")
            for file in files:
                f.write(f"- {file}\n")
            f.write("\n## Subdirectories:\n")
            for subdir in subdirs:
                f.write(f"- {subdir}\n")
            f.write(
                f"\n> There are {len(files)} files and {len(subdirs)} directories.\n"
            )
            f.write(f"Last update: {changes}")

        return True  # README created

    else:
        # Update README.md
        with open(readme_path, "w") as f:
            f.write("# Directory Listing\n\n")
            f.write(f"Directory: {directory}\n\n")
            f.write("## Files:\n")
            for file in files:
                f.write(f"- {file}\n")
            f.write("\n## Subdirectories:\n")
            for subdir in subdirs:
                f.write(f"- {subdir}\n")
            f.write(
                f"\n> There are {len(files)} files and {len(subdirs)} directories.\n"
            )
            f.write(f"Last update: {changes}")

        return False  # README updated


def process_readme_files(directory, changes):
    """Scan through directories and create or update README files where necessary."""
    readme_created_count = 0
    readme_updated_count = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip hidden directories and files
        dirnames[:] = [
            d for d in dirnames if not d.startswith(".")
        ]  # Skip hidden directories
        filenames = [f for f in filenames if not f.startswith(".")]  # Skip hidden files

        subdirs = dirnames
        files = filenames

        # Check if README exists
        readme_path = os.path.join(dirpath, "README.md")
        if not os.path.exists(readme_path):
            create_or_update_readme(dirpath, files, subdirs, changes)
            readme_created_count += 1
            log_event("INFO", f"README created in {dirpath}")
        else:
            create_or_update_readme(dirpath, files, subdirs, changes)
            readme_updated_count += 1
            log_event("INFO", f"README updated in {dirpath}")

    return readme_created_count, readme_updated_count


def generate_readme_content(directory, files, subdirectories):
    """Generate content for the README.md file."""
    content = f"# Directory listing for {os.path.basename(directory)}\n\n"
    content += "## Files:\n"
    if files:
        for file in files:
            content += f"- {file}\n"
    else:
        content += "None\n"

    content += "\n## Subdirectories:\n"
    if subdirectories:
        for subdir in subdirectories:
            content += f"- {subdir}\n"
    else:
        content += "None\n"

    return content


def manage_readme_files(directory):
    """Manage README.md files in the directory and subdirectories."""
    readme_created_count = 0
    readme_updated_count = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        # Skip hidden directories and files
        dirnames[:] = [
            d for d in dirnames if not d.startswith(".")
        ]  # Skip hidden directories
        filenames = [f for f in filenames if not f.startswith(".")]  # Skip hidden files

        # Check if README.md exists
        readme_path = os.path.join(dirpath, "README.md")
        if not os.path.exists(readme_path):
            create_or_update_readme(dirpath, filenames, dirnames)
            readme_created_count += 1
        else:
            create_or_update_readme(dirpath, filenames, dirnames)
            readme_updated_count += 1

    return readme_created_count, readme_updated_count
