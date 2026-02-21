# Module_4: Testing & Documentation
Tonya Capillo | JHED ID: 174BAB | Due Feb 17, 2026 11:59 PM EST | SSH url: git@github.com/tcapillo28/jhu_software_concepts.git

## Overview 
This project implements a lightweight Flask application built specifically for Module 4.  
Before beginning this module, I encountered several issues while testing my Module 3 application.  
To support the testing goals of Module 4, I built a lightweight Flask application that includes two simplified buttons (“Pull Data” and “Update Analysis”).
These endpoints were intentionally minimal so their POST behavior, state updates, and analysis formatting could be tested reliably with pytest. 
This approach allowed me to practice route testing, button testing, and integration testing without relying on the unfinished Module 3 scraper and database.

Multiple components in Module 3 require further review, including:

- generating the database correctly  
- ensuring the scraper collects all required fields (GPA, GRE, comments, etc.)  
- producing an `llm_extend_applicant_data.json` file that matches the structure of the professor’s example  
- verifying that the “Pull Data” and “Update Analysis” buttons function end‑to‑end  

Because these gaps prevented reliable testing, I paused work on the Module 3 test suite until the underlying functionality can be corrected.

For Module 4, Copilot recommended building a minimal Flask application with a faux database layer.  
This allowed me to focus on understanding the testing framework itself — isolated routes, predictable utility functions, and a clean environment for pytest — without being blocked by the unresolved Module 3 issues.

The result is a small, self‑contained Flask app designed to demonstrate:

- clean project structure  
- functional routing  
- a simple in‑memory or JSON‑based storage layer  
- a fully passing pytest suite  
- Sphinx documentation generated from the codebase  

This module intentionally avoids the complexity of Module 3 so that the testing concepts can be learned and exercised.
The application is intentionally minimal: it exposes a small set of routes, performs simple computations, and provides a predictable surface for automated testing and documentation.

---

## Documentation
Full project documentation is available on Read the Docs:
https://jhu-software-concepts-module-4-tc.readthedocs.io/en/latest/

## How to Run the Application
Follow these steps to start the Flask server locally:

1. **Activate your virtual environment**
    ```bash
   source venv/bin/activate        # macOS/Linux
   venv\Scripts\activate           # Windows
2. **Install dependencies**
    ```bash
   pip install -r requirements.txt
3. **Run the Flask app**
    ```bash
   flask --app app run
4. **Open the application in browser**
    ``bash
    http://127.0.0.1:5000/

## Running Tests
All tests use pytest and are designed to run cleanly without external dependencies.
Run options: 
1. Run the full suite:
    ```bash 
    pytest -q
2. Run tests by marker:
    ```bash
    pytest -m web
    pytest -m utils
    pytest -m integration
3. Run test by keyword:
    ```bash
    pytest -k route
    pytest -k compute
4. Run with coverage:
    ```bash
    pytest --cov=app --cov-report=term-missing

## Project Structure

module_4/
├── docs/                     # Sphinx documentation (source + build)
├── src/
│   ├── templates/            # HTML templates for Flask
│   │   └── analysis.html         # Analysis page template
│   ├── __init__.py
│   ├── analysis.py           # Analysis logic used by the app
│   ├── app.py                # Main Flask application
│   ├── load_data.py          # Faux database / data loading helpers
│   ├── scrape.py             # Placeholder scraper logic (Module 3 reference)
│   └── state.py              # Simple state management for the faux DB
├── tests/
│   ├── conftest.py
│   ├── test_analysis_format.py
│   ├── test_buttons.py
│   ├── test_db_insert.py
│   ├── test_flask_page.py
│   └── test_integration_end_to_end.py
├── venv/                     # Virtual environment (not submitted)
├── .coverage                 # Coverage data file
├── pytest.ini                # Pytest configuration
├── README.md                 # Project documentation
├── actions_success.png       # Screenshot of successful GitHub Actions run
├── img.png                   # Additional screenshot or image asset
├── coverage_summary.txt      # Coverage report summary
└── requirements.txt          # Python dependencies

## Architecture and Design Decisions
The architecture for Module 4 is intentionally minimal. The goal of this module was not to build a full production system, but to create a clean, testable Flask application that demonstrates routing, state handling, and analysis logic in a controlled environment.

Key design choices:

- **Lightweight Flask Application**  
  The app exposes only the routes required for testing. This keeps the behavior predictable and easy to validate.

- **Faux Database Layer**  
  Instead of integrating a real database, the project uses simple JSON/state helpers. This avoids external dependencies and ensures tests run consistently.

- **Separation of Concerns**  
  - `app.py` handles routing  
  - `analysis.py` contains analysis logic  
  - `load_data.py` and `state.py` manage faux‑database operations  
  - `templates/` contains HTML output  
  This separation makes each component independently testable.

- **Test‑Driven Structure**  
  The project layout was chosen to support pytest fixtures, route testing, and integration tests without relying on Module 3’s incomplete functionality.

- **Module 3 Isolation**  
  Module 3’s scraper and database generation require further fixes, so Module 4 was built independently to ensure the testing concepts could be demonstrated correctly.

## API Summary
This section provides a high-level overview of the routes and core functions implemented in the Module 4 application.

### Routes

- **GET /**  
  Renders the main page and displays the current state of the faux database.

- **POST /pull**  
  Simulates pulling new data into the faux database. Used for testing button behavior.

- **POST /update_analysis**  
  Runs the analysis logic and updates the analysis output. Tested for correct formatting and state changes.

- **GET /analysis**  
  Renders the `analysis.html` template showing the formatted analysis results.

### Core Logic

- **analysis.py**  
  Contains the formatting and computation logic used to generate the analysis output.

- **load_data.py**  
  Handles reading and writing faux‑database content.

- **state.py**  
  Maintains simple in‑memory state for testing workflows.

These components are intentionally simple so the testing suite can focus on correctness, formatting, and workflow behavior.

## Known Limitations
This Module 4 application is intentionally minimal and does not include:

- a real database or persistent storage  
- a fully functional scraper  
- integration with Module 3’s data pipeline  
- production-level error handling  
- complex routing or multi-step workflows  

Additionally, Module 3 requires further review before its test suite can be completed:

- the scraper does not collect all required fields (GPA, GRE, comments, etc.)
- the database generation step is incomplete
- the resulting `llm_extend_applicant_data.json` file does not match the professor’s example
- the “Pull Data” and “Update Analysis” buttons do not function correctly in Module 3 due to upstream issues

These issues prevented reliable testing in Module 3, which is why Module 4 uses simplified button endpoints designed specifically for testing.

## Future Improvements
Planned next steps include:

- Fixing the Module 3 scraper to collect all required fields  
- Regenerating the database to match the expected schema  
- Ensuring the `llm_extend_applicant_data.json` output matches the professor’s example  
- Debugging the Pull/Update buttons in Module 3 so they work end‑to‑end  
- Expanding the Module 4 application to include:
  - real database integration
  - additional routes and workflows
  - more robust analysis logic
  - integration tests that simulate real user behavior
  - improved UI templates for clarity and usability