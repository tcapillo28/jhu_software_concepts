"""
Scraping interface placeholder for Module 4.

This module defines the public scraping function used by the Flask
application. In the real world, this function would fetch and parse
external data. However, for Module 4, the function is intentionally
minimal because the test suite mocks it to supply controlled rows.

The purpose of this module is to provide a stable interface so that:

- ``app.py`` can call ``scrape.load_rows()`` without knowing the details.
- The pytest suite can patch ``load_rows`` to return predictable data.
- Sphinx can generate API documentation for the scraping layer.

No network requests or parsing logic are implemented here.
"""


def load_rows():
    """
    Return placeholder scraped rows.

    In Module 4, this function is never used to perform real scraping.
    Instead, the test suite replaces it with a mock that returns
    controlled test data. The default implementation simply returns
    an empty list so the application can run without errors.

    Returns:
        list[dict]: An empty list unless replaced by a test mock.
    """

    return []
