from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json


def fetch_html(page):
    url = f"https://www.thegradcafe.com/survey/?page={page}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(req).read().decode("utf-8")


def parse_table(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    results = []

    if not table:
        return results

    rows = table.find_all("tr")

    # Skip header row
    for row in rows[1:]:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]

        if len(cols) < 5:
            continue

        entry = {
            "school": cols[0],
            "program": cols[1],
            "added_on": cols[2],
            "decision": cols[3],
            "notes": cols[4]
        }

        results.append(entry)

    return results


if __name__ == "__main__":
    all_data = []

    # Fetch first 5 pages (adjust if needed)
    for page in range(1, 6):
        print(f"Fetching page {page}...")
        html = fetch_html(page)
        page_data = parse_table(html)
        all_data.extend(page_data)

    with open("your_part_1.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2)

    print("Saved your_part_1.json")