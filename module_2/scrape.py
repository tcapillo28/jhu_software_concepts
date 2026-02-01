#1. Imports
from urllib.request import urlopen, Request
from urllib import parse, robotparser

from bs4 import BeautifulSoup


#2. robots.txt code compliance check
agent="Tonya"
url = "https://www.thegradcafe.com/"

def check_bots():
    parser = robotparser.RobotFileParser(url)
    parser.set_url(parse.urljoin(url, "/robots.txt"))
    parser.read()

    paths = [
        "/",
        "/cgi-bin/",
        "/admin/",
        "survey/?page=1"
        ]

    print("Robots.txt file checks:")
    for path in paths:
        print(f'{parser.can_fetch(agent, path), path}')
    return parser


# 3. fetch HTML page

def fetch_html_page(page=1):
    url = f"https://www.thegradcafe.com/survey/?page={page}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urlopen(req).read().decode("utf-8")
    return html

# 4. parse HTML table
# 5. main scraping loop
# 6. save to JSON
# 7. run fuctions:

if __name__ == "__main__":
    check_bots()
    html = fetch_html_page(1)
    print("fetched HTML length:", len(html))