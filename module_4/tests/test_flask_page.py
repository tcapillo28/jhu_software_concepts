import pytest
from src.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_analysis_page_loads(client):
    response = client.get("/analysis")
    assert response.status_code == 200
    html = response.data.decode()

    assert "Analysis" in html
    assert "Pull Data" in html
    assert "Update Analysis" in html
    assert "Answer:" in html

def test_root_redirects(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (301, 302)