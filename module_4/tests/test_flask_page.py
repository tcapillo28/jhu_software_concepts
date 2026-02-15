import pytest

@pytest.mark.web
def test_analysis_page_loads(client):
    response = client.get("/analysis")
    assert response.status_code == 200
    html = response.data.decode()

    assert "Analysis" in html
    assert "Pull Data" in html
    assert "Update Analysis" in html
    assert "Answer:" in html