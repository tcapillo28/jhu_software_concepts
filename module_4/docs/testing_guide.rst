Testing Guide
=============

This page explains how to run the test suite for Module 4, how to use
markers and selectors, and the test doubles used to isolate components.

Running the Test Suite
----------------------

All tests use ``pytest``. To run the full suite:

::

    pytest -q

To run with coverage:

::

    pytest -q --cov=src --cov-report=term-missing


Marker-Based Test Selection
---------------------------

Tests are organized using assignment-required markers:

- ``web`` – HTML structure and route responses
- ``buttons`` – pull/update button behavior
- ``analysis`` – analysis output and formatting
- ``db`` – in-memory database behavior
- ``integration`` – end-to-end flows

Run tests by marker:

::

    pytest -m web
    pytest -m buttons
    pytest -m "analysis or db"
    pytest -m integration

Run all marked tests:

::

    pytest -m "web or buttons or analysis or db or integration"


Selector-Based Filtering
------------------------

Selectors allow running tests by keyword:

::

    pytest -k pull
    pytest -k analysis
    pytest -k "pull and not busy"

This is useful for debugging specific behaviors.


Test Doubles and Fixtures
-------------------------

The test suite uses lightweight test doubles to isolate components.

Mocked Scraper
~~~~~~~~~~~~~~
``scrape.load_rows`` is patched in tests to return controlled rows.
This prevents network calls and ensures deterministic behavior.

Mocked Analysis
~~~~~~~~~~~~~~~
``analysis.compute_analysis`` is patched to return predictable output.
This allows route behavior to be tested independently of analysis logic.

In-Memory Database Reset
~~~~~~~~~~~~~~~~~~~~~~~~
The global list in ``load_data`` is cleared between tests to avoid
cross-test contamination.

Flask Test Client
~~~~~~~~~~~~~~~~~
Tests use Flask’s built-in test client to issue requests and inspect
HTML responses without running a live server.


Expected Behavior Under Test
----------------------------

- ``/pull-data`` sets the busy flag, inserts rows, and redirects.
- ``/update-analysis`` calls ``compute_analysis`` and updates the page.
- Busy-state logic prevents overlapping operations.
- The HTML page includes required labels and percentages.
- The in-memory database behaves predictably under inserts and reads.