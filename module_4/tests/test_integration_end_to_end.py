import pytest
from src.load_data import db_session


@pytest.mark.integration
def test_end_to_end_flow(client, mocker):
    fake_rows = [
        {"id": 1, "program": "CS"},
        {"id": 2, "program": "Biology"}
    ]
    mocker.patch("src.load_data.load_rows", return_value=fake_rows)

    # Pull
    r1 = client.post("/pull-data")
    assert r1.status_code in (200, 202)
    assert db_session.count_rows() == 2

    # Update
    r2 = client.post("/update-analysis")
    assert r2.status_code == 200

    # Render
    r3 = client.get("/analysis")
    html = r3.data.decode()
    assert "Answer:" in html