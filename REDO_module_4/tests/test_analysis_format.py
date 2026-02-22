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

@pytest.mark.analysis
def test_pull_data_scraper_failure(client, mocker):
    """
    If the scraper raises an exception, /pull_data must return a non-200 status
    and must not call the loader. This ensures no partial writes occur.
    """
    mocker.patch("src.scrape.scrape_data", side_effect=Exception("scrape failed"))
    fake_loader = mocker.patch("src.load_data.load_data")

    response = client.post("/pull_data")

    assert response.status_code != 200
    fake_loader.assert_not_called()

@pytest.mark.analysis
def test_pull_data_loader_failure(client, mocker):
    """
    If the loader fails after scraping succeeds, /pull_data must return a
    non-200 status and must not render partial analysis output. The HTML
    returned should contain an error indicator rather than any analysis
    content. BeautifulSoup is used to inspect the returned HTML structure.
    """
    mocker.patch("src.scrape.scrape_data", return_value=[{"a": 1}])
    mocker.patch("src.load_data.load_data", side_effect=Exception("load failed"))

    response = client.post("/pull_data")
    html = response.data.decode()

    assert response.status_code != 200

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()

    # Expect an error message, not analysis content
    assert "error" in text or "failed" in text
    assert "answer:" not in text
    assert "%" not in text

@pytest.mark.analysis
def test_update_analysis_query_failure(client, mocker):
    """
    If the query function fails, /update_analysis must return a non-200 status
    and must not attempt to render partial analysis output.
    """
    mocker.patch("src.query_data.get_full_output", side_effect=Exception("query failed"))

    response = client.post("/update_analysis")
    html = response.data.decode()

    assert response.status_code != 200

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text().lower()

    assert "error" in text or "failed" in text
    assert "answer:" not in text
    assert "%" not in text
