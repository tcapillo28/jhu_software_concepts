import pytest

@pytest.mark.db
def test_get_full_output_coverage(mocker):
    # Mock DB connection
    mock_conn = mocker.patch("src.query_data.get_connection")
    mock_cursor = mock_conn.return_value.cursor.return_value

    # Fake rows for each query
    mock_cursor.fetchall.side_effect = [
        [("A", 1)],   # Q1
        [("B", 2)],   # Q2
        [("C", 3)],   # Q3
        [("D", 4)],   # Q4
        [("E", 5)],   # Q5
        [("F", 6)],   # Q6
        [("G", 7)],   # Q7
        [("H", 8)],   # Q8
        [("I", 9)],   # Q9
    ]

    from src.query_data import get_full_output
    text = get_full_output()

    # Ensure all 9 questions appear
    for i in range(1, 10):
        assert f"Question {i}" in text