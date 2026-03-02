Testing Guide
=============

This project includes a comprehensive pytest suite with 100% coverage.

Running Tests
-------------
Run all tests:

.. code-block:: bash

   pytest -q

Markers
-------
- web
- buttons
- analysis
- db
- integration

Fixtures & Fakes
----------------
The test suite uses fakes for database state and mocks for busy-state logic.