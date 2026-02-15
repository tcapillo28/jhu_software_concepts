import pytest

@pytest.mark.buttons
def test_pull_data_success(client, mocker):
    fake_rows = [{"id": 1, "program": "CS"}]
    mocker.patch("src.load_data.load_rows", return_value=fake_rows)

    response = client.post("/pull-data")
    assert response.status_code in (200, 202)
    assert response.json.get("ok") is True

@pytest.mark.buttons
def test_update_analysis_when_busy(client, mocker):
    mocker.patch("src.state.is_busy", return_value=True)

    response = client.post("/update-analysis")
    assert response.status_code == 409
    assert response.json.get("busy") is True