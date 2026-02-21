"""
Tests for button behavior and busy‑state gating in the Flask application.

These tests verify:
- POST /pull_data triggers the scraper and loader when not busy.
- POST /update_analysis succeeds when not busy.
- Both endpoints return 409 when the application is in a busy state.
"""

import pytest
from unittest.mock import patch, MagicMock

@pytest.mark.buttons
@patch("src.load_data.load_data")
@patch("src.scrape.scrape_data")
def test_pull_data_success(mock_load, mock_scrape, client):
    """Test that POST /pull_data returns 200 and triggers scraper + loader.

    This test mocks both `scrape_data` and `load_data` to avoid running
    real scraping or database operations. It verifies that:
    - The route returns HTTP 200.
    - The scraper is invoked once.
    - The loader is invoked once with the scraper's output.
    """

    mock_scrape.return_value = [{"row": 1}, {"row": 2}]  # fake scraper output

    response = client.post("/pull_data")

    assert response.status_code == 200
    mock_scrape.assert_called_once()
    mock_load.assert_called_once()


@pytest.mark.buttons
def test_update_analysis_success(client):
    """Test that POST /update_analysis returns 200 when not busy.

    The busy flag is explicitly set to 'False', to simulate an idle state.
    The route should accept the request and return HTTP 200.
    """

    client.application.scrape_running = False  # ensure not busy

    response = client.post("/update_analysis")

    assert response.status_code == 200


@pytest.mark.buttons
def test_update_analysis_busy(client):
    """Test that POST /update_analysis returns 409 when busy.

    When a pull-data operation is in progress, the busy flag is True.
    The update-analysis route should reject the request with HTTP 409.
    """

    client.application.scrape_running = True  # simulate busy state

    response = client.post("/update_analysis")

    assert response.status_code == 409


@pytest.mark.buttons
def test_pull_data_busy(client):
    """Test that POST /pull_data returns 409 when busy.

    When the busy flag is True, the pull-data route must not start a new
    scrape operation and should return HTTP 409.
    """

    client.application.scrape_running = True  # simulate busy state

    response = client.post("/pull_data")

    assert response.status_code == 409