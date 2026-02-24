"""
In‑memory storage utilities for Module 4.

This module provides a minimal fake database used for testing and for the
Flask application. Instead of writing a real database,
rows are stored in a module‑level list named ``_db``.

The test suite interacts with this module by:
- mocking the scraper to supply controlled rows
- calling ``insert_rows`` to append new entries
- calling ``get_all_rows`` to retrieve the current state

The goal is to provide a predictable, lightweight storage
layer for the assignment.
"""

# In-memory "database"
_db = []

def insert_rows(rows):
    """
    Insert new rows into the in‑memory database.

    This function appends the provided rows to the global ``_db`` list.
    The behavior is intentionally simple because the test suite controls
    the input via mocks. It performs no deduplication, validation, or transformation of rows.

    Args:
        rows (list[dict]): A list of row dictionaries to store.

    Returns:
        None
    """

    global _db
    _db.extend(rows)

def get_all_rows():
    """
    Retrieve all stored rows.

    Returns a copy of the internal list so callers cannot
    mutate the underlying storage unintentionally.

    Returns:
        list[dict]: All rows currently stored in the in‑memory database.
    """

    return list(_db)