import pytest
from src.app import create_app
import src.analysis as analysis
from unittest.mock import patch


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_compute_analysis_returns_string():
    result = analysis.compute_analysis()
    assert isinstance(result, str)
    assert len(result) > 0

def test_analysis_page_includes_result(client):
    response = client.get("/analysis")
    html = response.data.decode()
    assert "Answer:" in html

def test_update_analysis_returns_json(client):
    response = client.post("/update-analysis")
    assert response.status_code == 200
    assert "analysis" in response.json

def test_update_analysis_busy(client):
    with patch("src.app.state.is_busy", return_value=True):
        response = client.post("/update-analysis")
        assert response.status_code == 409
        assert response.json == {"error": "busy"}


def test_pull_data_busy(client):
    with patch("src.state.is_busy", return_value=True):
        response = client.post("/pull-data")
        assert response.status_code == 409
        assert response.json == {"error": "busy"}

