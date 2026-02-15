import pytest
import json
import os

# ---------------------------------------------------------
# FIXTURE 1: Flask test client (you already had this)
# ---------------------------------------------------------
from app import create_app

@pytest.fixture
def client():
    """
    Creates a fresh Flask test client for each test.

    Why:
    - Allows tests to call your routes ("/", "/pull_data", etc.)
      without running the real server.
    - create_app(testing=True) ensures TESTING mode is enabled.
    """
    app = create_app(testing=True)
    return app.test_client()


# ---------------------------------------------------------
# FIXTURE 2: Reset saved_data.json before each test
# ---------------------------------------------------------
@pytest.fixture
def reset_saved_data():
    """
    Ensures each test starts with a clean dataset.

    Why:
    - Your scraper and loader write to saved_data.json.
    - If tests share leftover data, they will interfere with each other.
    - This fixture clears the file before each test that uses it.
    """
    # Path to saved_data.json inside src/
    path = os.path.join(os.path.dirname(__file__), "..", "src", "saved_data.json")

    # Overwrite the file with an empty list
    with open(path, "w") as f:
        json.dump([], f)

    yield  # run the test

    # Optional: clean again after the test
    with open(path, "w") as f:
        json.dump([], f)


# ---------------------------------------------------------
# FIXTURE 3: Fake scraper output for mocking
# ---------------------------------------------------------
@pytest.fixture
def fake_scrape_output():
    """
    Provides a reusable fake dataset for tests that need
    predictable scraper results.

    Why:
    - Your real scraper hits GradCafe and takes time.
    - Tests must be fast and deterministic.
    - Tests will patch scrape.scrape_data to return this instead.
    """
    return [
        {"id": 1, "program": "CS", "decision": "Accepted"},
        {"id": 2, "program": "Biology", "decision": "Rejected"},
    ]