import io
import sys
import psycopg2
import os


def get_connection():
    """Return a DB connection using DATABASE_URL if available."""
    url = os.getenv("DATABASE_URL")
    if url:
        return psycopg2.connect(url)

    # Local fallback for development
    return psycopg2.connect(
        dbname="gradcafe",
        user="postgres",
        password="2828",
        host="localhost",
        port=5432
    )


def get_full_output():
    """Run all SQL queries and capture printed output."""
    buffer = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = buffer

    try:
        conn = get_connection()
        cur = conn.cursor()

        # ---------------------------------------------------------
        #   Question 1
        # ---------------------------------------------------------
        print("\nQuestion 1. Number of Fall 2026 applicants:")
        q1 = """
        SELECT COUNT(*)
        FROM applicants
        WHERE term = 'Fall 2026';
        """
        cur.execute(q1)
        print(cur.fetchone()[0])

        print("\nQuestion 1.A) What are the number of entries/applicants for each term?")
        q_all_terms = """
        SELECT DISTINCT term, COUNT(*) AS num_entries
        FROM applicants
        GROUP BY term
        ORDER BY term;
        """
        cur.execute(q_all_terms)
        for term, count in cur.fetchall():
            print(f"{term}: {count}")

        conn.close()

    finally:
        sys.stdout = original_stdout

    return buffer.getvalue()

    # ---------------------------------------------------------
    #   Question 2
    # ---------------------------------------------------------
    print("\nQuestion 2. Percentage of entries from international students:")
    q2 = """
    SELECT 
        ROUND(
            (SUM(CASE WHEN us_or_international = 'International' THEN 1 ELSE 0 END)::numeric 
            / COUNT(*) * 100)
        , 2)
    FROM applicants;
    """
    cur.execute(q2)
    print(str(cur.fetchone()[0]) + "%")

    print("\nQuestion 2.A) What are the total entries by citizenship category?")
    q_cit_counts = """
    SELECT 
        us_or_international,
        COUNT(*) AS total_entries
    FROM applicants
    GROUP BY us_or_international
    ORDER BY us_or_international;
    """
    cur.execute(q_cit_counts)
    for category, total in cur.fetchall():
        print(f"{category}: {total}")

    # ---------------------------------------------------------
    #   Question 3
    # ---------------------------------------------------------
    print("\nQuestion 3. Average GPA, GRE, GRE V, and GRE AW (excluding missing values):")
    q3 = """
    SELECT
        ROUND(AVG(gpa)::numeric, 2),
        ROUND(AVG(gre)::numeric, 2),
        ROUND(AVG(gre_v)::numeric, 2),
        ROUND(AVG(gre_aw)::numeric, 2)
    FROM applicants;
    """
    cur.execute(q3)
    avg_gpa, avg_gre, avg_gre_v, avg_gre_aw = cur.fetchone()
    print(f"Average GPA: {avg_gpa}")
    print(f"Average GRE Total: {avg_gre}")
    print(f"Average GRE Verbal: {avg_gre_v}")
    print(f"Average GRE AW: {avg_gre_aw}")

    # ---------------------------------------------------------
    #   Question 4
    # ---------------------------------------------------------
    print("\nQuestion 4: Average GPA of American students in Fall 2026:")
    q4 = """
    SELECT
        ROUND(AVG(gpa)::numeric, 2)
    FROM applicants
    WHERE us_or_international = 'American'
      AND term = 'Fall 2026';
    """
    cur.execute(q4)
    print(cur.fetchone()[0])

    # ---------------------------------------------------------
    #   Question 5
    # ---------------------------------------------------------
    print("\nQuestion 5. Percent of Fall 2026 entries that are Acceptances:")
    q5 = """
    SELECT 
        ROUND(
            (SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END)::numeric 
            / COUNT(*) * 100)
        , 2)
    FROM applicants
    WHERE term = 'Fall 2026';
    """
    cur.execute(q5)
    print(str(cur.fetchone()[0]) + "%")

    # ---------------------------------------------------------
    #   Question 6
    # ---------------------------------------------------------
    print("\nQuestion 6. Average GPA of Accepted applicants in Fall 2026:")
    q6 = """
    SELECT
        ROUND(AVG(gpa)::numeric, 2)
    FROM applicants
    WHERE term = 'Fall 2026'
      AND status = 'Accepted';
    """
    cur.execute(q6)
    print(cur.fetchone()[0])

    # ---------------------------------------------------------
    #   Question 7
    # ---------------------------------------------------------
    print("\nQuestion 7. Number of JHU Master's in Computer Science applicants:")
    q7 = """
    SELECT COUNT(*) AS jhu_cs_masters_count
    FROM applicants
    WHERE llm_generated_university = 'Johns Hopkins University'
      AND degree = 'Masters'
      AND llm_generated_program = 'Computer Science';
    """
    cur.execute(q7)
    print(cur.fetchone()[0])

    # ---------------------------------------------------------
    #   Question 8
    # ---------------------------------------------------------
    print("\nQuestion 8. Accepted 2026 PhD CS applicants to Georgetown, MIT, Stanford, or CMU (LLM fields):")
    q8 = """
    SELECT COUNT(*) AS accepted_2025_top4_phd_cs
    FROM applicants
    WHERE term LIKE '%2026'
      AND status = 'Accepted'
      AND degree = 'PhD'
      AND llm_generated_program LIKE 'Computer Science'
      AND llm_generated_university LIKE ANY (ARRAY[
            '%Georgetown%',
            '%Massachusetts Institute of Technology%',
            '%MIT%',
            '%Stanford%',
            '%Carnegie Mellon%'
      ]);
    """
    cur.execute(q8)
    print(cur.fetchone()[0])

    # ---------------------------------------------------------
    #   Question 9
    # ---------------------------------------------------------
    print("\nQuestion 9 result: Accepted 2026 PhD CS applicants using RAW fields:")
    q9_raw = """
    SELECT COUNT(*) AS raw_accepted_2025_top4_phd_cs
    FROM applicants
    WHERE term LIKE '%2026'
      AND status = 'Accepted'
      AND degree = 'PhD'
      AND program ILIKE '%Computer%'
      AND (
            program ILIKE '%Georgetown%'
         OR program ILIKE '%MIT%'
         OR program ILIKE '%Massachusetts Institute of Technology%'
         OR program ILIKE '%Stanford%'
         OR program ILIKE '%Carnegie Mellon%'
      );
    """
    cur.execute(q9_raw)
    print(cur.fetchone()[0])

    print("\n=== INTERPRETATION FOR QUESTION 9 ===")
    print(
        "Using the LLM‑generated fields (Question 8), I found 22 accepted 2025 PhD Computer Science applicants to the four target universities. "
        "Using the raw scraped fields with substring matching (Question 9), the count increased to 50.\n"
        "This difference occurs because the raw program field is significantly noisier and contains inconsistent formatting, abbreviations, and concatenated text. "
        "When using ILIKE with broad substrings (e.g., '%Computer%', '%MIT%'), many additional entries are matched that would not be considered true CS PhD applications. "
        "The LLM‑generated fields are more standardized, so the filtering is more precise and produces a lower, more accurate count."
    )

    cur.close()
    conn.close()

    # ---------------------------------------------------------
    # RESTORE STDOUT AND RETURN TEXT
    # ---------------------------------------------------------
    sys.stdout = original_stdout
    return buffer.getvalue()