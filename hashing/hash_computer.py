#!/usr/bin/env python3

import hashlib


def compute_file_hash(file_path):
    """Compute the hash for a file."""
    hash_obj = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()
