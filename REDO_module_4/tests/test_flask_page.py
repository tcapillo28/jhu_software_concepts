"""
Tests for the Flask application’s basic routing and page rendering.

This module verifies that the Flask app created by ``create_app`` exposes the
required Module 4 routes and that the ``/analysis`` page renders successfully.
These tests ensure that the application factory pattern is implemented
correctly and that the HTML template includes the required UI elements
specified in the assignment.

The tests in this module do not interact with the database, scraper, or
analysis logic. They only validate Flask routing and template rendering.
"""

import pytest

@pytest.mark.web
def test_app_factory(client):
    """
    Verify that the Flask application factory registers the required routes.

    This test inspects the application's URL map to confirm that the Module 4
    API endpoints are present. These include:

    * ``/analysis`` – GET route for rendering the static instance of the analysis page.
    * ``/pull-data`` – POST route for initiating a data pull (mocked in tests).
    * ``/update-analysis`` – POST route for triggering an analysis update.

    The presence of these routes ensures that the application is structured
    according to the Module 4 specification and that the test suite can
    interact with the app through the expected endpoints.
    """

    # Ensure the Flask app loads and routes are registered
    routes = [rule.rule for rule in client.application.url_map.iter_rules()]

    # Module-4 required routes
    assert "/analysis" in routes
    assert "/pull_data" in routes
    assert "/update_analysis" in routes


@pytest.mark.web
def test_analysis_page_loads(client):
    """
    Ensure that the ``/analysis`` page loads successfully and contains the
    required UI elements.

    This test sends a GET request to the analysis page and verifies:

    * HTTP 200 response status.
    * Presence of the required text elements:
        - ``Analysis`` (page header)
        - ``Pull Data`` (button label)
        - ``Update Analysis`` (button label)
        - ``Answer:`` (label for analysis output)

    These elements are required for later tests that validate formatting,
    button behavior, and analysis rendering. This test confirms that the
    template is correctly structured and that the route renders without error.
    """

    response = client.get("/analysis")
    assert response.status_code == 200

    html = response.data.decode()

    # Required UI elements
    assert "Analysis" in html
    assert "Pull Data" in html
    assert "Update Analysis" in html
    assert "Answer:" in html