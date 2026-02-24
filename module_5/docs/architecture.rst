Architecture
============

The Module 4 application is organized into three layers: a web layer,
an ETL layer, and a lightweight in‑memory database layer. Each layer is
intentionally simple so the test suite can isolate components and mock
behavior as needed.

Web Layer (Flask)
-----------------

The web layer is implemented in ``app.py`` and provides the user-facing
interface. Its responsibilities include:

- Rendering the main HTML page.
- Handling user actions such as pulling data and updating analysis.
- Calling into the ETL and analysis layers.
- Enforcing the busy‑state policy to prevent overlapping operations.

Routes include:

- ``/`` – Display the current analysis and action buttons.
- ``/pull-data`` – Trigger a data pull and update the in‑memory database.
- ``/update-analysis`` – Recompute and display analysis results.

The web layer does not perform scraping, storage, or analysis directly.
Instead, it delegates to the underlying modules.

ETL Layer
---------

The ETL layer consists of two modules:

- ``scrape.py`` – Provides ``load_rows()``, a placeholder scraper
  function. In real applications this would fetch external data, but in
  Module 4 it is always mocked by the test suite.
- ``load_data.py`` – Provides ``insert_rows()`` and ``get_all_rows()``,
  which manage the in‑memory storage list.

Responsibilities of the ETL layer:

- Define the interface for retrieving new rows.
- Provide a simple mechanism for loading rows into storage.
- Allow the test suite to patch scraper output for deterministic tests.

Database Layer (In‑Memory Storage)
----------------------------------

Instead of a real database, Module 4 uses a module‑level list in
``load_data.py`` to store rows. This keeps the application lightweight
and easy to test.

Responsibilities:

- Store rows inserted by the ETL layer.
- Return a copy of stored rows to prevent accidental mutation.
- Provide predictable behavior for the test suite.

Analysis Layer
--------------

The analysis layer is implemented in ``analysis.py`` and provides a
single function:

- ``compute_analysis()`` – Returns a placeholder analysis string.

In a full application, this layer would compute statistics based on
stored rows. For Module 4, the function is intentionally minimal so that
tests can mock it and verify route behavior independently.

Busy-State Tracking
-------------------

The ``state.py`` module provides a simple busy‑state flag used by the
web layer to prevent overlapping operations.

Responsibilities:

- ``is_busy()`` – Check whether an operation is in progress.
- ``set_busy(value)`` – Mark the system as busy or idle.

This avoids race conditions during ``/pull-data`` and
``/update-analysis`` without requiring real concurrency primitives.