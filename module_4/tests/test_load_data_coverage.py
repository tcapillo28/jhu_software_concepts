import pytest

@pytest.mark.db
def test_insert_rows_coverage(mocker):
    mock_conn = mocker.patch("src.load_data.get_connection")
    mock_cursor = mock_conn.return_value.cursor.return_value

    rows = [{"id": 1, "program": "CS"}]

    from src.load_data import insert_rows
    insert_rows(rows)

    # Ensure execute was called at least once
    assert mock_cursor.execute.called