import pytest
from src.load_data import insert_rows, _db

@pytest.mark.db
def test_insert_rows_coverage():
    # Reset the in-memory DB
    _db.clear()

    rows = [
        {"id": 1, "program": "CS"},
        {"id": 2, "program": "Math"},
    ]

    insert_rows(rows)

    # Should now contain both rows
    assert len(_db) == 2

    # Insert duplicates
    insert_rows([{"id": 1, "program": "CS"}])

    # Should still be 2 because duplicates are skipped
    assert len(_db) == 2