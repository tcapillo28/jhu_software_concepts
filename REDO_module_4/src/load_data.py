# -----------------------------------------------------------------------------------
# Script created using llm_extend_applicant_data.json from Liv.
# Using Windows psycopg2
# To change the input file. Go to bottom of this file in main and insert the full file path
# ___________________________________________________________________________________

import json
import datetime
from datetime import datetime


def clean_float(value):
    """
    Extracts a numeric float from messy strings like 'GPA 3.89' from .json.
    Returns None if no valid number is found.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value

    import re
    match = re.search(r"(\d+(\.\d+)?)", str(value))
    if match:
        return float(match.group(1))
    return None


def clean_date(date_str):
    """
    Converts dates like 'January 31, 2026' into YYYY-MM-DD format.
    Returns None if the date is missing or invalid.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except ValueError:
        return None


def strip_nul(value):
    """Remove NUL bytes from strings."""
    if isinstance(value, str):
        return value.replace("\x00", "")
    return value


def load_data(json_path):
    """
    Opens the database, reads cleaned JSON, inserts every record into PostgreSQL.
    """
    import psycopg2 # <-- moved here so Module 4 tests don’t import it

    # 1. Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="gradcafe",
        user="postgres",
        password="2828",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    # 2. Load JSON file safely (handles NUL bytes and unknown encodings)
    clean_lines = []
    with open(json_path, "rb") as f:
        for raw_line in f:
            raw_line = raw_line.replace(b"\x00", b"")  # remove NUL bytes
            line = raw_line.decode("utf-8", errors="ignore").strip()
            if line:
                clean_lines.append(line)

    # Parse each JSON object (line-delimited JSON)
    data = [json.loads(line) for line in clean_lines]

    # 3. Insert each row
    for row in data:
        cur.execute(
            """
            INSERT INTO applicants (
                program,
                comments,
                date_added,
                url,
                status,
                term,
                us_or_international,
                gpa,
                gre,
                gre_v,
                gre_aw,
                degree,
                llm_generated_program,
                llm_generated_university
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                strip_nul(row.get("program")),
                strip_nul(row.get("comments")),
                clean_date(strip_nul(row.get("date_added"))),
                strip_nul(row.get("url")),
                strip_nul(row.get("applicant_status")),
                strip_nul(row.get("semester_year_start")),
                strip_nul(row.get("citizenship")),
                clean_float(strip_nul(row.get("gpa"))),
                clean_float(strip_nul(row.get("gre"))),
                clean_float(strip_nul(row.get("gre_v"))),
                clean_float(strip_nul(row.get("gre_aw"))),
                strip_nul(row.get("masters_or_phd")),
                strip_nul(row.get("llm-generated-program")),
                strip_nul(row.get("llm-generated-university"))
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Data successfully loaded into applicants table.")


if __name__ == "__main__":
    load_data(r"C:\Users\tonya\PycharmProjects\jhu_software_concepts\module_3\llm_extend_applicant_data_Provided.json")