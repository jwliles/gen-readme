#!/usr/bin/env python3

import os


def scan_directories(directory):
    """Scan subdirectories within the given directory."""
    subdirs = [
        d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))
    ]
    return subdirs
