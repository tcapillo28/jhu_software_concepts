"""
In‑memory busy‑state tracking for Module 4.

This module provides a lightweight mechanism for preventing overlapping
operations in the Flask application. The busy flag is stored inside the
module‑level dictionary ``BUSY_STATE`` so that tests can easily patch or
inspect it without requiring a real concurrency primitive.

The busy flag is used by:
- ``/pull-data`` to prevent concurrent data pulls
- ``/update-analysis`` to avoid recomputing analysis during a pull

Because the assignment runs in a single‑threaded test environment, this
implementation intentionally avoids locks, semaphores, or other
synchronization constructs. Mutating the dictionary value is sufficient
for ensuring predictable behavior during testing.
"""

BUSYSTATE = {"value":False}

def is_busy():
    """
    Check whether the system is currently marked as busy.

    Returns:
        bool: True if a scrape or update operation is in progress,
        False otherwise.
    """

    return BUSYSTATE["value"]

def set_busy(value: bool):
    """
    Set the busy state.

    Args:
        value (bool): The new busy state. True marks the system as busy,
        False marks it as idle.

    Returns:
        None
    """

    global BUSYSTATE
    BUSYSTATE["value"] = value
