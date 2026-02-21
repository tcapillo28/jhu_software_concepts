import sys
import os

# Ensure project root is on the Python path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.app import create_app
import pytest

@pytest.fixture
def client():
    '''
    Pytest loads app factory, tests run in testing mode
    and no real scraper or analysis is triggered
    '''
    app = create_app(testing=True)
    return app.test_client()