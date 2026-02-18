import pytest
from src.load_data import _db
from src.load_data import get_all_rows
from src.load_data import db_session


@pytest.mark.db
def test_insert_rows(client, mocker):
    _db.clear()   # reset DB at start of test

    mocker.patch("src.load_data.load_rows", return_value=[
        {"id": 1, "program": "CS", "decision": "Accepted"}
    ])

    # Before pull
    assert len(get_all_rows()) == 0

    # After pull
    client.post("/pull-data")
    assert len(get_all_rows()) == 1


@pytest.mark.db
def test_idempotency(client, mocker):
    _db.clear()   # reset DB at start of test

    fake = [{"id": 1, "program": "CS"}]
    mocker.patch("src.load_data.load_rows", return_value=fake)

    client.post("/pull-data")
    client.post("/pull-data")

    assert db_session.count_rows() == 1