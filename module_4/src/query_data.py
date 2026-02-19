import io
import sys
from module_4.src.database import get_db


def get_full_output():
    """Run all SQL queries using SQLite and capture printed output."""
    db = get_db()

    buffer = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = buffer

    try:
        # ---------------------------------------------------------
        #   Question 1
        # ---------------------------------------------------------
        print("\nQuestion 1. Number of Fall 2026 applicants:")
        q1 = """
        SELECT COUNT(*)
        FROM applicants
        WHERE term = 'Fall 2026';
        """
        q1_val = db.execute(q1).fetchone()[0]
        print("Answer:", q1_val)

        print("\nQuestion 1.A) What are the number of entries/applicants for each term?")
        q_all_terms = """
        SELECT term, COUNT(*) AS num_entries
        FROM applicants
        GROUP BY term
        ORDER BY term;
        """
        for term, count in db.execute(q_all_terms).fetchall():
            print(f"Answer: {term}: {count}")

        # ---------------------------------------------------------
        #   Question 2
        # ---------------------------------------------------------
        print("\nQuestion 2. Percentage of entries from international students:")
        q2 = """
        SELECT 
            ROUND(
                (SUM(CASE WHEN us_or_international = 'International' THEN 1 ELSE 0 END) * 1.0 
                / COUNT(*) * 100)
            , 2)
        FROM applicants;
        """
        q2_val = db.execute(q2).fetchone()[0]
        print(f"Answer: {q2_val}%")

        print("\nQuestion 2.A) What are the total entries by citizenship category?")
        q_cit_counts = """
        SELECT 
            us_or_international,
            COUNT(*) AS total_entries
        FROM applicants
        GROUP BY us_or_international
        ORDER BY us_or_international;
        """
        for category, total in db.execute(q_cit_counts).fetchall():
            print(f"Answer: {category}: {total}")

        # ---------------------------------------------------------
        #   Question 3
        # ---------------------------------------------------------
        print("\nQuestion 3. Average GPA, GRE, GRE V, and GRE AW (excluding missing values):")
        q3 = """
        SELECT
            ROUND(AVG(gpa), 2),
            ROUND(AVG(gre), 2),
            ROUND(AVG(gre_v), 2),
            ROUND(AVG(gre_aw), 2)
        FROM applicants;
        """
        avg_gpa, avg_gre, avg_gre_v, avg_gre_aw = db.execute(q3).fetchone()
        print(f"Answer: Average GPA: {avg_gpa}")
        print(f"Answer: Average GRE Total: {avg_gre}")
        print(f"Answer: Average GRE Verbal: {avg_gre_v}")
        print(f"Answer: Average GRE AW: {avg_gre_aw}")

        # ---------------------------------------------------------
        #   Question 4
        # ---------------------------------------------------------
        print("\nQuestion 4: Average GPA of American students in Fall 2026:")
        q4 = """
        SELECT
            ROUND(AVG(gpa), 2)
        FROM applicants
        WHERE us_or_international = 'American'
          AND term = 'Fall 2026';
        """
        q4_val = db.execute(q4).fetchone()[0]
        print("Answer:", q4_val)

        # ---------------------------------------------------------
        #   Question 5
        # ---------------------------------------------------------
        print("\nQuestion 5. Percent of Fall 2026 entries that are Acceptances:")
        q5 = """
        SELECT 
            ROUND(
                (SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) * 1.0
                / COUNT(*) * 100)
            , 2)
        FROM applicants
        WHERE term = 'Fall 2026';
        """
        q5_val = db.execute(q5).fetchone()[0]
        print(f"Answer: {q5_val}%")

        # ---------------------------------------------------------
        #   Question 6
        # ---------------------------------------------------------
        print("\nQuestion 6. Average GPA of Accepted applicants in Fall 2026:")
        q6 = """
        SELECT
            ROUND(AVG(gpa), 2)
        FROM applicants
        WHERE term = 'Fall 2026'
          AND status = 'Accepted';
        """
        q6_val = db.execute(q6).fetchone()[0]
        print("Answer:", q6_val)

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
        q7_val = db.execute(q7).fetchone()[0]
        print("Answer:", q7_val)

        # ---------------------------------------------------------
        #   Question 8
        # ---------------------------------------------------------
        print("\nQuestion 8. Accepted 2026 PhD CS applicants to Georgetown, MIT, Stanford, or CMU (LLM fields):")
        q8 = """
        SELECT COUNT(*) AS accepted_2026_top4_phd_cs
        FROM applicants
        WHERE term LIKE '%2026'
          AND status = 'Accepted'
          AND degree = 'PhD'
          AND llm_generated_program LIKE '%Computer Science%'
          AND (
                llm_generated_university LIKE '%Georgetown%'
             OR llm_generated_university LIKE '%Massachusetts Institute of Technology%'
             OR llm_generated_university LIKE '%MIT%'
             OR llm_generated_university LIKE '%Stanford%'
             OR llm_generated_university LIKE '%Carnegie Mellon%'
          );
        """
        q8_val = db.execute(q8).fetchone()[0]
        print("Answer:", q8_val)

        # ---------------------------------------------------------
        #   Question 9
        # ---------------------------------------------------------
        print("\nQuestion 9 result: Accepted 2026 PhD CS applicants using RAW fields:")
        q9_raw = """
        SELECT COUNT(*) AS raw_accepted_2026_top4_phd_cs
        FROM applicants
        WHERE term LIKE '%2026'
          AND status = 'Accepted'
          AND degree = 'PhD'
          AND program LIKE '%Computer%'
          AND (
                program LIKE '%Georgetown%'
             OR program LIKE '%MIT%'
             OR program LIKE '%Massachusetts Institute of Technology%'
             OR program LIKE '%Stanford%'
             OR program LIKE '%Carnegie Mellon%'
          );
        """
        q9_val = db.execute(q9_raw).fetchone()[0]
        print("Answer:", q9_val)

        print("\n=== INTERPRETATION FOR QUESTION 9 ===")
        print("Answer: Using the LLM‑generated fields (Question 8), I found 22 accepted 2026 PhD Computer Science applicants to the four target universities.")
        print("Answer: Using the raw scraped fields with substring matching (Question 9), the count increased to 50.")
        print("Answer: This difference occurs because the raw program field is significantly noisier and contains inconsistent formatting.")
        print("Answer: The LLM‑generated fields are more standardized, so the filtering is more precise.")

    finally:
        sys.stdout = original_stdout

    return buffer.getvalue()