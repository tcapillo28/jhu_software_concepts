import json
import re
import time
import os
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


# Global counter to track number of processed entries
global_count = 0

def load_rows():
    """
    Placeholder function required for tests.
    Tests patch this function to return fake scraped rows.
    """
    return []


# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def scrape_data(pages=2, max_entries=30000):

    """
    Scrapes multiple pages from GradCafe and returns raw entries.
    Use main.py to limit the amount of scraped data.
    A hard cap (max_entries) prevents exceeding assignment limits.
    """
    all_data = []

    for page in range(1, pages + 1):
        print(f"Fetching page {page}...")
        html = _fetch_html(page)
        page_data = _parse_table(html)

        # Add entries form this page
        all_data.extend(page_data)

        # Hard stop: do not exceed assignment limit
        if len(all_data) >= max_entries:
            print(f"Reached {max_entries} entries. Stopping scrape.")
            all_data = all_data[:max_entries]   # trim if slightly over
            break


        # Stop condition: no entries found on this page
        if not page_data:
            print(f"No entries found on page {page}. Stopping scrape.")
            break

    print(f"\nTotal entries scraped: {global_count}")
    return all_data


def save_data(new_entries):
    existing = load_existing_entries()

    # Build a set of unique keys for fast duplicate checking
    existing_keys = {
        (e.get("institution"), e.get("program"), e.get("date_added"))
        for e in existing
    }

    # Keep only entries that are NOT already in the file
    filtered = [
        entry for entry in new_entries
        if (entry.get("institution"), entry.get("program"), entry.get("date_added")) not in existing_keys
    ]

    # Append only new entries
    updated = existing + filtered

    with open("saved_data.json", "w") as f:
        json.dump(updated, f, indent=2)

    print(f"Saved {len(filtered)} NEW entries")

def load_existing_entries():
    if not os.path.exists("saved_data.json"):
        return []
    with open("saved_data.json", "r") as f:
        return json.load(f)
# ============================================================
# PRIVATE HELPERS
# ============================================================

def _fetch_html(page):
    url = f"https://www.thegradcafe.com/survey/?page={page}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urlopen(req).read().decode("utf-8")


def _parse_table(html):
    global global_count

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    results = []

    if not table:
        return results

    rows = table.find_all("tr")

    for row in rows[1:]:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue

        school_name = cells[0].get_text(strip=True)

        # URL
        url = None
        for tag in cells[-1].find_all("a"):
            href = tag.get("href")
            if href and "/result/" in href:
                url = href
                break

        if url and url.startswith("/"):
            url = "https://www.thegradcafe.com" + url

        # Comments + Stats
        comments = []
        stats = {
            "gpa": None,
            "gre_total": None,
            "gre_v": None,
            "gre_q": None,
            "gre_aw": None,
            "citizenship": None,
            "term": None
        }

        if url:
            comments = _fetch_comments(url)
            stats = _fetch_stats(url)

        # Program + Degree
        program_raw = cells[1].get_text(strip=True)
        program_name, degree_type = _split_program_and_degree(program_raw)

        # Added On
        added_on = cells[2].get_text(strip=True)

        # Decision + Date
        decision_raw = cells[3].get_text(strip=True)
        status, decision_date = _split_decision(decision_raw)

        entry = {
            "school": school_name,
            "url": url,
            "program": program_name,
            "degree_type": degree_type,
            "added_on": added_on,
            "applicant_status": status,
            "decision_date": decision_date,
            "comments": comments,
            "gpa": stats["gpa"],
            "gre_total": stats["gre_total"],
            "gre_v": stats["gre_v"],
            "gre_q": stats["gre_q"],
            "gre_aw": stats["gre_aw"],
            "citizenship": stats["citizenship"],
            "term": stats["term"]
        }

        global_count += 1
 #       print(f"Processed entry #{global_count}")

        results.append(entry)

    return results


def _fetch_comments(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        comment_blocks = soup.find_all("div", class_="comment-body")
        return [block.get_text(strip=True) for block in comment_blocks]

    except Exception:
        return None # Might need to adjust this to return null or ""


def _fetch_stats(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        html = urlopen(req).read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")

        stat_blocks = soup.find_all("div", class_="tw-text-sm tw-text-gray-600")
        stats_text = " ".join(block.get_text(" ", strip=True) for block in stat_blocks)

        gpa = re.search(r"GPA[:\s]+([0-4]\.\d{1,2})", stats_text)
        gre_total = re.search(r"GRE[:\s]+(\d{3})", stats_text)
        gre_v = re.search(r"V\s*(\d{2,3})", stats_text)
        gre_q = re.search(r"Q\s*(\d{2,3})", stats_text)
        gre_aw = re.search(r"AW\s*([0-6]\.?\d?)", stats_text)
        citizenship = re.search(r"(International|American)", stats_text, re.IGNORECASE)
        term = re.search(r"(Fall|Spring|Summer|Winter)\s+\d{4}", stats_text)

        return {
            "gpa": gpa.group(1) if gpa else None,
            "gre_total": gre_total.group(1) if gre_total else None,
            "gre_v": gre_v.group(1) if gre_v else None,
            "gre_q": gre_q.group(1) if gre_q else None,
            "gre_aw": gre_aw.group(1) if gre_aw else None,
            "citizenship": citizenship.group(1) if citizenship else None,
            "term": term.group(0) if term else None
        }

    except Exception:
        return {
            "gpa": None,
            "gre_total": None,
            "gre_v": None,
            "gre_q": None,
            "gre_aw": None,
            "citizenship": None,
            "term": None
        }


def _split_program_and_degree(text):
    degree_keywords = ["PhD", "Masters", "Master", "MS", "MA", "MEng", "MPH", "MBA"]

    for degree in degree_keywords:
        if text.endswith(degree):
            program = text[: -len(degree)].strip()
            return program, degree

    return text, None


def _split_decision(text):
    if " on " in text:
        status, date = text.split(" on ", 1)
        return status.strip(), date.strip()
    return text.strip(), None


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    start_time = time.time()

    data = scrape_data(pages=100)
    save_data(data)

    end_time = time.time()
    print(f"Total runtime: {end_time - start_time:.2f} seconds")