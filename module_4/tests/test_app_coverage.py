import pytest

@pytest.mark.web
def test_index_route_coverage(client, mocker):
    mocker.patch("src.app.get_full_output", return_value="Question 1\nAnswer 1")
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.web
def test_analysis_route_coverage(client, mocker):
    mocker.patch("src.app.get_full_output", return_value="Question 1\nAnswer 1")
    response = client.get("/analysis")
    assert response.status_code == 200