import pytest
from src.app import create_app

@pytest.fixture
def client():
    '''
    Pytest loads app factory, tests run in testing mode
    and no real scraper or anlaysis is triggered
    '''
    app = create_app(testing=True)
    return app.test_client()