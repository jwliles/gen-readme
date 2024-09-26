#!/usr/bin/env python3

import os
import hashlib

def write_readme(directory, files, subdirs, date_str):
    """Write the README.md file for the given directory."""
    readme_path = os.path.join(directory, "README.md")
    new_content = [
        f"<!-- hash:{hashlib.md5(''.join(files).encode('utf-8')).hexdigest()} -->\n",
        "# README\n\n",
    ]

    if files:
        new_content.append(f">There are {len(files)} notes in this directory as of {date_str}\n\n")

    new_content.append("---\n\n")

    if subdirs:
        new_content.append("## Categories\n\n")
        for subdir in subdirs:
            new_content.append(f"- [{subdir.capitalize()}](./{subdir})\n")
        new_content.append("\n---\n\n")

    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(new_content)

