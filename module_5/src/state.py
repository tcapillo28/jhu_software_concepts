"""
In‑memory busy‑state tracking for Module 4.

This module provides a minimal mechanism for preventing overlapping
operations in the Flask application. The state is stored in a simple
boolean variable named ``_busy`` so that tests can easily patch or
inspect it.

The busy flag is used by:
- ``/pull-data`` to prevent concurrent data pulls
- ``/update-analysis`` to avoid recomputing analysis during a pull

This implementation intentionally avoids any concurrency primitives
because the assignment runs in a single‑threaded test environment.
"""

_busy = False

def is_busy():
    """
    Check whether the system is currently marked as busy.

    Returns:
        bool: True if a scrape or update operation is in progress,
        False otherwise.
    """

    return _busy

def set_busy(value: bool):
    """
    Set the busy state.

    Args:
        value (bool): The new busy state. True marks the system as busy,
        False marks it as idle.

    Returns:
        None
    """

    global _busy
    _busy = value
