import pytest
from src.app import create_app
import src.analysis as analysis

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