from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json
# 1. HELPER FUNCTIONS GO HERE
def split_program_and_degree(text):
    degree_keywords = ["PhD", "Masters", "Master", "MS", "MA", "MEng", "MPH", "MBA"]

    for degree in degree_keywords:
        if text.endswith(degree):
            program = text[: -len(degree)].strip()
            return program, degree

    # If no degree found
    return text, None


# 2. HTML FETCH FUNCTION
def fetch_html(page):
    url = f"https://www.thegradcafe.com/survey/?page={page}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(req).read().decode("utf-8")

# 3. PARSER FUNCTION
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

            # Extract program + degree
        program_raw = cols[1]
        program_name, degree_type = split_program_and_degree(program_raw)

        entry = {
            "school": cols[0],
            "program": program_name,
            "degree_type": degree_type,
            "added_on": cols[2],
            "decision": cols[3]
        }

        results.append(entry)

    return results

# 4. MAIN SCRIPT
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