# -----------------------------------------------------------------------------------
# Script was creating using llm_extend_applicant_data.json from Liv.
# Using Windows psycopg2
# ___________________________________________________________________________________


import json
import psycopg2
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
    Converts dates like 'January 31, 2026' into YYYY-MM-DD format
    (PostgreSQL required format YYYY-MM-DD)
    Returns None if the date is missing or invalid.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%B %d, %Y").date()
    except ValueError:
        return None


def load_data(json_path):
    """
    Opens the database, reads cleaned llm_extended_applicant_data.json and
    inserts every record and saves the data into the applicants table in PostgreSQL.
    Then closes the connection.
    """
    # 1. Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="gradcafe",
        user="postgres",
        password="2828",
        host="localhost",
        port=5432
    )
    cur = conn.cursor()

    # 2. Load JSON file
    with open(json_path, "r", encoding="utf-16") as f:
        data = [json.loads(line) for line in f]  # your file is line-delimited JSON

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
                row.get("program"),
                row.get("comments"),
                clean_date(row.get("date_added")),
                row.get("url"),
                row.get("applicant_status"),
                row.get("semester_year_start"),
                row.get("citizenship"),
                clean_float(row.get("gpa")),
                clean_float(row.get("gre")),
                clean_float(row.get("gre_v")),
                clean_float(row.get("gre_aw")),
                row.get("masters_or_phd"),
                row.get("llm-generated-program"),
                row.get("llm-generated-university")
            )
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Data successfully loaded into applicants table.")


if __name__ == "__main__":
    load_data(r"C:\Users\tonya\PycharmProjects\jhu_software_concepts\module_2\llm_extend_applicant_data.json")