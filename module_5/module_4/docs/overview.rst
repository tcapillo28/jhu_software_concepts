Overview & Setup
================

This project implements a minimal web application for Module 4. The app
provides a simple ETL workflow, an in‑memory database, and a placeholder
analysis layer. The goal is to demonstrate clean separation of concerns,
testability, and Sphinx documentation.

Running the Application
-----------------------

The application is a small Flask web server. To run it locally:

1. Activate your virtual environment::

       source venv/bin/activate        # macOS/Linux
       venv\Scripts\activate           # Windows

2. Install dependencies::

       pip install -r requirements.txt

3. Start the Flask app::

       flask --app app run

4. Open the browser at::

       http://127.0.0.1:5000/

The home page displays the current analysis results and provides buttons
to pull new data and recompute analysis.

Required Environment Variables
------------------------------

The application does not use a real database for Module 4. Instead, it
stores rows in an in‑memory list. However, the assignment requires
documenting environment variables, so the following placeholder variable
is included for completeness:

- ``DATABASE_URL`` – Not used in Module 4, but included to match typical
  ETL application structure.

Running the Test Suite
----------------------

All tests use ``pytest`` and are organized using assignment‑required
markers. To run the full suite:

::

    pytest -q

To run tests by marker:

::

    pytest -m web
    pytest -m buttons
    pytest -m "analysis or db"
    pytest -m integration

To filter tests by keyword:

::

    pytest -k pull
    pytest -k analysis

To run with coverage:

::

    pytest -q --cov=src --cov-report=term-missing

Project Structure
-----------------

The project is organized into three layers:

- **Web layer (Flask)** – Handles routes, user actions, and HTML
  rendering.
- **ETL layer (scrape → load_data)** – Provides a mock scraper and an
  in‑memory storage module.
- **Analysis layer** – Computes placeholder analysis results for display.

These layers are intentionally simple so the test suite can isolate and
mock each component.