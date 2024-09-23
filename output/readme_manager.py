#!/usr/bin/env python3
import os
from logs.event_logger import log_event


def process_or_manage_readme_files(directory, changes):
    """Ensure README.md files are created or updated for each directory."""
    readme_created_count = 0
    readme_updated_count = 0

    for dirpath, dirnames, filenames in os.walk(directory):
        log_event("DEBUG", f"Processing directory: {dirpath}")
        dirnames[:] = [
            d for d in dirnames if not d.startswith(".")
        ]  # Skip hidden directories
        filenames = [f for f in filenames if not f.startswith(".")]  # Skip hidden files

        readme_path = os.path.join(dirpath, "README.md")

        # Check if README exists
        if not os.path.exists(readme_path):
            # Create README
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# Directory Listing for {dirpath}\n\n")
                f.write("## Files:\n")
                for file in filenames:
                    f.write(f"- {file}\n")
                f.write("\n## Subdirectories:\n")
                for subdir in dirnames:
                    f.write(f"- {subdir}\n")
                f.write(
                    f"\n> There are {len(filenames)} files and {len(dirnames)} directories in {dirpath}.\n"
                )
                f.write(f"Last update: {changes}\n")
            readme_created_count += 1
        else:
            # Check if the content has actually changed before updating
            with open(readme_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

            new_content = (
                f"# Directory Listing for {dirpath}\n\n"
                f"## Files:\n"
                + "".join(f"- {file}\n" for file in filenames)
                + f"\n## Subdirectories:\n"
                + "".join(f"- {subdir}\n" for subdir in dirnames)
                + f"\n> There are {len(filenames)} files and {len(dirnames)} directories in {dirpath}.\n"
                f"Last update: {changes}\n"
            )

            if existing_content != new_content:
                # Only update if the content is different
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                readme_updated_count += 1

    return readme_created_count, readme_updated_count
