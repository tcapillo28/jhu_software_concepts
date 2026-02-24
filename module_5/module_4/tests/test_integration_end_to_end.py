import pytest
from unittest.mock import patch
from src.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.integration
def test_full_flow(client):
    # Step 1: GET /analysis (page loads)
    response = client.get("/analysis")
    assert response.status_code == 200

    # Step 2: POST /pull-data (mock ETL)
    fake_rows = [{"program": "CS", "result": "Accepted"}]

    with patch("src.scrape.load_rows", return_value=fake_rows) as mock_scrape:
        with patch("src.load_data.insert_rows") as mock_insert:
            response = client.post("/pull-data")
            assert response.status_code == 200
            mock_scrape.assert_called_once()
            mock_insert.assert_called_once_with(fake_rows)

    # Step 3: POST /update-analysis (mock compute_analysis)
    with patch("src.analysis.compute_analysis", return_value="Mocked Result"):
        response = client.post("/update-analysis")
        assert response.status_code == 200
        assert response.json["analysis"] == "Mocked Result"