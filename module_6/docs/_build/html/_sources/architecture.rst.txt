Architecture
============

The application consists of several layers that work together to scrape, store,
analyze, and display Grad Café admissions data.

Web Layer (Flask)
-----------------
Serves the analysis page and exposes endpoints for pulling data and updating analysis.

ETL Layer
---------
Handles scraping, cleaning, and loading Grad Café entries into the database.

Database Layer
--------------
Stores rows and supports analysis queries through SQL functions.