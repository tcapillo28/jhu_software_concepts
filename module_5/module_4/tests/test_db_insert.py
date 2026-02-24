import pytest
from unittest.mock import patch
from src.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

@pytest.mark.db
def test_pull_data_inserts_rows(client):
    # Mock scrape.load_rows() to return fake rows
    fake_rows = [{"program": "CS", "result": "Accepted"}]

    with patch("src.scrape.load_rows", return_value=fake_rows) as mock_scrape:
        with patch("src.load_data.insert_rows") as mock_insert:
            response = client.post("/pull-data")

            # Ensure the route succeeded
            assert response.status_code == 200

            # Ensure scrape.load_rows() was called
            mock_scrape.assert_called_once()

            # Ensure insert_rows() was called with the fake rows
            mock_insert.assert_called_once_with(fake_rows)

@pytest.mark.db
def test_load_data_functions():
    from src import load_data

    load_data._db.clear()
    load_data.insert_rows([{"x": 1}])
    rows = load_data.get_all_rows()

    assert rows == [{"x": 1}]

@pytest.mark.db
def test_scrape_load_rows():
    from src.scrape import load_rows
    assert load_rows() == []