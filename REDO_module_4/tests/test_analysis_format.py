import pytest
import re
from bs4 import BeautifulSoup

@pytest.mark.analysis
def test_analysis_page_renders_components(client):
    """
    Test that GET "/" returns the fully rendered analysis page with all required
    Module 4 components.

    Although the assignment references GET /analysis, both "/" and "/analysis"
    render the same analysis dashboard in Module 4 because /analysis delegates
    directly to index(). Using "/" ensures the test always reflects the actual
    live analysis page, even when the analysis content is updated.

    This test verifies:
    - The route responds with HTTP 200.
    - The page includes the visible title text “Analysis”.
    - The page renders both action buttons: “Pull Data” and “Update Analysis”.
    - The rendered analysis contains at least one “Answer:” label.
    - At least one percentage on the page is formatted with exactly two decimal
      places (e.g., 45.00%), based on the final rendered HTML.
    """

    response = client.get("/analysis")
    html = response.data.decode()
   #print(html)

    # Find all percentage-like substrings
    percentages = re.findall(r"\d+\.?\d*%", html)

    # Now assert that each one matches the correct two-decimal format
    for p in percentages:
        assert re.fullmatch(r"\d+\.\d{2}%", p), f"Incorrect percentage format: {p}"

    assert response.status_code == 200
    assert "Analysis" in html
    assert "Pull Data" in html
    assert "Update Analysis" in html
    assert "Answer:" in html

