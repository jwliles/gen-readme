#!/usr/bin/env python3

import hashlib
import logging
import os
from datetime import datetime

# Template for README (you can enable this later)
README_TEMPLATE = """
# {directory_name}

This directory contains the following files:

{file_list}

Generated on: {date}
"""

# Function to create a README file for a specific directory
def create_readme_file(directory, files, subdirs, date_str, use_template=False):
    """Creates a README.md file for the given directory."""
    readme_path = os.path.join(directory, "README.md")

    if use_template:
        # Template-based README generation
        file_list = "\n".join(f"- {file}" for file in files)
        new_content = README_TEMPLATE.format(
            directory_name=os.path.basename(directory),
            file_list=file_list,
            date=date_str
        )
    else:
        # Basic README content
        new_content = [
            f"<!-- hash:{hashlib.md5(''.join(files).encode('utf-8')).hexdigest()} -->\n",
            "# README\n\n",
            f">This directory contains {len(files)} files as of {date_str}\n\n",
            "---\n\n",
            "## Files\n\n"
        ]
        if files:
            new_content.extend([f"- {file}\n" for file in files])
        if subdirs:
            new_content.append("\n## Subdirectories\n\n")
            for subdir in subdirs:
                new_content.append(f"- [{subdir.capitalize()}](./{subdir})\n")

    with open(readme_path, "w", encoding="utf-8") as f:
        if use_template:
            f.write(new_content)  # Template is a string
        else:
            f.writelines(new_content)  # Basic version is a list

    print(f"Generated README for {directory}")

# Recursive function to generate README files for all directories and subdirectories
def generate_all_readme_files(directory, changes, metrics, use_template=False):
    """Recursively generates README.md files for all directories."""
    try:
        # List subdirectories and files
        subdirs = [
            d for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]
        files = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]

        # Track processed directory
        metrics.increment_files_scanned()

        # Generate the README for the current directory
        logging.debug(f"Generating README for {directory}")
        date_str = datetime.now().strftime("%Y-%m-%d")

        # Assume write_readme will return True if the README is created or updated
        if create_readme_file(directory, files, subdirs, date_str, use_template):
            metrics.increment_readme_created() if changes else metrics.increment_readme_updated()

        # Recursively handle subdirectories
        for subdir in subdirs:
            subdir_path = os.path.join(directory, subdir)
            generate_all_readme_files(subdir_path, changes, metrics, use_template)

    except Exception as e:
        logging.error(f"Error generating README for {directory}: {e}")
        metrics.increment_skipped_files()
