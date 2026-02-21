# Module_4: Testing & Documentation
Tonya Capillo | JHED ID: 174BAB | Due Feb 17, 2026 11:59 PM EST | SSH url: git@github.com:tcapillo28/jhu_software_concepts.git

## Overview 
This project implements a lightweight Flask application built specifically for Module 4.  
Before beginning this module, I encountered several issues while testing my Module 3 application.  
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
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
├── tests/
│   ├── test_routes.py
│   └── conftest.py
├── docs/
│   ├── source/
│   │   ├── index.rst
│   │   ├── overview.rst
│   │   ├── architecture.rst
│   │   ├── api_reference.rst
│   │   ├── testing_guide.rst
│   │   ├── operational_notes.rst
│   │   └── modules.rst
│   └── Makefile
├── requirements.txt
└── README.md
