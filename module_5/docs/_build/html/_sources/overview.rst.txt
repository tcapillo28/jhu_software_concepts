Overview & Setup
================

This documentation provides an overview of the Grad Café Analytics application,
including environment setup, running the application, and executing the test suite.

Environment Variables
---------------------
- DATABASE_URL: PostgreSQL connection string used by the application.

Running the Application
-----------------------
To run the Flask app locally:

1. Activate your virtual environment.
2. Start PostgreSQL.
3. Run:

   .. code-block:: bash

      flask --app src/app.py run

Running Tests
-------------
Use pytest to run the full suite:

.. code-block:: bash

   pytest -q