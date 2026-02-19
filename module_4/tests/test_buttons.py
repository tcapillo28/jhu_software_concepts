import pytest
from src.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_pull_data_button_exists(client):
    response = client.get("/analysis")
    html = response.data.decode()
    assert "Pull Data" in html

def test_update_analysis_button_exists(client):
    response = client.get("/analysis")
    html = response.data.decode()
    assert "Update Analysis" in html