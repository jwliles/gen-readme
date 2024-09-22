#!/usr/bin/env python3


def verify_file_hash(stored_hash, new_hash):
    """Verify if the stored hash matches the newly computed hash."""
    return stored_hash == new_hash
