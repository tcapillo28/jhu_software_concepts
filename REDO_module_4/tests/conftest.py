import pytest
import json
import os
import sys

# Add module_4 root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.app import create_app


@pytest.fixture
def client():
    app = create_app(testing=True)
    return app.test_client()


@pytest.fixture
def reset_saved_data():
    path = os.path.join(os.path.dirname(__file__), "..", "src", "saved_data.json")

    with open(path, "w") as f:
        json.dump([], f)

    yield

    with open(path, "w") as f:
        json.dump([], f)


@pytest.fixture
def fake_scrape_output():
    return [
        {"id": 1, "program": "CS", "decision": "Accepted"},
        {"id": 2, "program": "Biology", "decision": "Rejected"},
    ]


@pytest.fixture(autouse=True)
def mock_full_output(mocker, request):
    """
    Automatically mock get_full_output ONLY for GET requests.
    POST /update_analysis tests must be able to patch it themselves.
    """
    # If the test name contains "update_analysis" AND it's a POST test,
    # do NOT mock here — let the test control the patch.
    if "update_analysis" in request.node.name:
        return
    mocker.patch("src.query_data.get_full_output", return_value="Mocked output")
