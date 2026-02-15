import pytest
import re

@pytest.mark.analysis
def test_percentage_formatting(client):
    response = client.get("/analysis")
    html = response.data.decode()

    # Regex for two-decimal percentages
    pattern = r"\d+\.\d{2}%"
    assert re.search(pattern, html)