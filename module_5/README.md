# Module_5: Software Assurance + Secure SQL
Tonya Capillo | JHED ID: 174BAB | Due Feb 23, 2026 11:59 PM PST | SSH url: git@github.com/tcapillo28/jhu_software_concepts.git |
RTD URL: https://jhu-software-concepts-module-4-tc.readthedocs.io/en/latest/


## Overview
Module 5 extends the lightweight Flask application developed in Module 4 
by adding secure‑coding practices, dependency scanning, and continuous‑integration 
enforcement. The Module 4 application was intentionally minimal because several 
components of Module 3 (scraper, database generation, and end‑to‑end button behavior) 
required further fixes. To ensure reliable testing, Module 4 used a simplified 
faux‑database design with predictable routes and state transitions.

Module 5 builds on that foundation and introduces:
- secure coding and SQL‑injection defenses
- least‑privilege database configuration
- dependency scanning with Snyk
- CI enforcement using GitHub Actions
- automated linting, testing, and dependency‑graph generation
The goal is to “shift security left” by integrating security checks directly into the development workflow

## Step 2: Secure Coding Practices 
Secure Coding Practices (Step 2)
Module 5 does not use a real SQL database. All data is stored in memory using a Python list (). 
Because no SQL queries are constructed or executed, there is no injection surface in this module.
If the project were extended to use PostgreSQL, all queries would need to be constructed using
psycopg’s safe SQL‑composition utilities (, , ) to ensure proper parameterization.

## Step 3: Least Privilege Database Configuration
Although Module 5 does not connect to a real database, a .env.example file is included to
demonstrate how credentials would be supplied through environment variables. 
The real .env file is excluded via .gitignore to prevent committing secrets.
In a real deployment, the application would use a least‑privilege PostgreSQL user with only the
permissions required for its operations.

## Why Steps 2 and 3 Are Conceptual in this Module
Module 5 builds on the lightweight Flask application created in Module 4, which intentionally uses an in‑memory faux‑database instead of a real PostgreSQL instance. Because no SQL engine, cursor, or query construction exists in this module, there is no SQL injection surface and no database user to harden. As a result, Steps 2 and 3 are implemented conceptually rather than through code changes.
The security principles are still documented:
- Step 2 explains how SQL injection would be prevented if a real database layer were added (using psycopg’s safe SQL‑composition utilities).
- Step 3 demonstrates least‑privilege configuration through a .env.example file and secret‑management practices, even though no real credentials are used.
A real PostgreSQL integration will be introduced once Module 3’s scraper and database generation are corrected, at which point these defenses will be implemented in full.


## Step 6: Dependency Scanning with Snyk
Running'snyk test'
scanned 36 dependencies and identified two vulnerabilities:
- flask@3.1.2 — Low severity
- werkzeug@3.1.5 — Medium severity
Both were resolved by upgrading to the patched versions (flask@3.1.3, werkzeug@3.1.6)
- A second scan confirmed that all vulnerabilities were fixed. The screenshot is included as 

## Step 6 - Extra Credit
Running 'snyk code test' returned a 403 error because Snyk Code is not available for free‑tier organizations. 
The error screenshot is included for documentation.

## Step 7: CI with GitHub Actions
Continuous Integration with GitHub Actions (Step 7)
A GitHub Actions workflow (.github/workflows/ci.yml) enforces “shift‑left security” by running on every push and pull request. The workflow performs four checks:
- Pylint with --fail-under=10
- Dependency graph generation using pydeps + Graphviz
- Snyk dependency scan (non‑blocking)
- Pytest with 100% coverage enforcement
This ensures that linting, testing, dependency scanning, and dependency‑graph generation all run automatically in CI.

## How to  Run the Application 
1. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
2. Install dependencies
    ```bash
    pip install -r requirements.txt
3. Run the Flask app
    ```bash
    flask --app src/app run
4. Open in browser
http://127.0.0.1:5000/

## Running Test
1. Full Suite:
    ```bash
   pytest-q
2. By marker:
    ```bash
   pytest -m web
    pytest -m buttons
    pytest -m db
    pytest -m analysis
    pytest -m integration
3. With coverage:
    ```bash
     pytest --cov=src --cov-report=term-missing

## Running Pylint
    
    pylint src --fail-under=10

## Generating the Dependency Graph
    pydeps src --noshow -T svg -o dependency.svg

## Fresh Install
1. Using pip: This method uses Python’s standard virtual‑environment tools.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install --upgrade pip
    pip install -e .
    pip install -r requirements.txt
2. Using uv: This method uses uv to create and synchronize the environment.
If uv is not on PATH, call it using its full installation path.
    ```bash
    uv.exe venv venv
    .\venv\Scripts\activate
    uv.exe pip install -e .
    uv.exe pip sync requirements.txt

## API Summary
### Routes
- GET / — Displays current faux‑database state
- POST /pull — Simulates pulling new data
- POST /update_analysis — Runs analysis and updates output
- GET /analysis — Renders formatted analysis results

### Core logic
- analysis.py — formatting and computation
- load_data.py — faux‑database read/write
- state.py — in‑memory state management

## Known Limitations
- No real database or persistent storage
- No production‑level error handling
- Module 3’s scraper and database generation still require fixes
- Module 4/5 use simplified endpoints to support testing and security tooling

## Future Improvements
- Fix Module 3 scraper and regenerate database
- Integrate real PostgreSQL with least‑privilege roles
- Expand analysis logic
- Add more realistic workflows and UI improvements
- Extend CI to include type‑checking and static analysis
