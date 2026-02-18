import pytest
from unittest.mock import MagicMock

@pytest.mark.web
def test_scrape_module_runs(mocker):
    # Mock requests.get so no network call happens
    mocker.patch("src.scrape.requests.get", return_value=MagicMock(text="<html></html>"))

    # Import and run the scraper
    from src.scrape import scrape_data

    # Just ensure it executes without error
    scrape_data()