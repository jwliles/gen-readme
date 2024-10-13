#!/usr/bin/env python3

import os
import hashlib


def write_readme(directory, files, subdirs, date_str, use_template=False):
    readme_path = os.path.join(directory, "README.md")

    if use_template:
        # Example of template-based README generation
        template_content = f"# {os.path.basename(directory)}\n\n"
        template_content += (
            f"Contains {len(files)} files and {len(subdirs)} subdirectories.\n"
        )
        template_content += f"Generated on {date_str}."
        new_content = template_content
    else:
        new_content = [
            f"<!-- hash:{hashlib.md5(''.join(files).encode('utf-8')).hexdigest()} -->\n",
            "# README\n\n",
            f">There are {len(files)} files in this directory as of {date_str}\n\n",
            "---\n\n",
            "## Files\n\n",
        ]
        if files:
            new_content.extend([f"- {file}\n" for file in files])
        if subdirs:
            new_content.append("\n## Subdirectories\n\n")
            for subdir in subdirs:
                new_content.append(f"- [{subdir.capitalize()}](./{subdir})\n")

    with open(readme_path, "w", encoding="utf-8") as f:
        if use_template:
            f.write(new_content)
        else:
            f.writelines(new_content)

    print(f"Generated README for {directory}")
