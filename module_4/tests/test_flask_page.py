import pytest

@pytest.mark.web
def test_analysis_page_loads(client):
    """
    Tests that the main analysis page ("/") loads successfully.

    Why:
    - Ensures the route exists.
    - Ensures the template renders without errors.
    """

    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode()

    # These checks depend on your HTML template.

    assert "Analysis" in html # your tiles contain "Question X"

    assert "Pull Data" in html # your pull button text

    assert "Update Analysis" in html # your update button text
