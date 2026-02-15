import pytest
from src.flask_app import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    return app.test_client()