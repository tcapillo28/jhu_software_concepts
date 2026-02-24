"""
In‑memory storage utilities for Module 4.

This module implements a lightweight, list‑based storage layer used by both the
Flask application and the test suite. Instead of connecting to a real database,
rows are accumulated in the module‑level list ``_db`` so that tests can easily
control, inspect, and reset application state.

The test suite interacts with this module by:
- mocking the scraper to supply controlled rows
- calling ``insert_rows`` to append new entries
- calling ``get_all_rows`` to retrieve the current state

A placeholder variable named ``db_session_value`` is also defined because earlier
versions of the assignment used a real database session, and the test suite still
imports this symbol. It is intentionally set to ``None`` and unused by the
current in‑memory implementation.

This design keeps the storage layer predictable, isolated, and fully compatible
with the single‑threaded test environment used in the assignment.
"""

# IN-MEMORY DATABASE SESSION
_db = []            # creates fake database
DB_SESSION = None

def insert_rows(rows):
    """
    Insert new rows into the in‑memory database.

    This function appends the provided rows to the  ``_db`` list.
    The behavior is intentionally simple because the test suite controls
    the input via mocks. It performs no deduplication, validation, or transformation of rows.

    Args:
        rows (list[dict]): A list of row dictionaries to store.

    Returns:
        None
    """

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
