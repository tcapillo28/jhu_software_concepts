import psycopg2

"""
Connect to PostgreSQL database

"""
conn = psycopg2.connect(
    dbname="gradcafe",
    user="postgres",
    password="2828",
    host="localhost",
    port=5432
)
cur = conn.cursor()


# -------------------------------------------------------------------------------------------------------
#   Questions 1:
# -------------------------------------------------------------------------------------------------------

"""
Inspect available terms and total entries for each term
"""

print("\n--- Number of entries for each term---")
q_all_terms = """
SELECT DISTINCT term, COUNT(*) AS num_entries
FROM applicants
GROUP BY term
ORDER BY term;
"""
cur.execute(q_all_terms)
rows = cur.fetchall()
for term, count in rows:
    print(f"{term}: {count}")



"""
QUESTION 1: How many entries do you have in your database who have applied for Fall 2025?
"""
q1 = """
SELECT COUNT(*)
FROM applicants
WHERE term = 'Fall 2025';
"""


cur.execute(q1)
print("\nQuestion 1. Number of Fall 2025 applicants:", cur.fetchone()[0])


# -------------------------------------------------------------------------------------------------------
#   Questions 2:
# -------------------------------------------------------------------------------------------------------


"""
What are the distinct citizenship categories?
"""

print("\n--- Total entries by citizenship category ---")
q_cit_counts = """
SELECT 
    us_or_international,
    COUNT(*) AS total_entries
FROM applicants
GROUP BY us_or_international
ORDER BY us_or_international;
"""
cur.execute(q_cit_counts)
rows = cur.fetchall()
for category, total in rows:
    print(f"{category}: {total}")


"""
Question 2: What percentage of entries are from international students (not American or Other) (to two decimal places)?
"""

q2 = """
SELECT 
    ROUND(
        (SUM(CASE WHEN us_or_international = 'International' THEN 1 ELSE 0 END)::numeric 
        / COUNT(*) * 100)
    , 2) AS pct_international
FROM applicants;
"""
cur.execute(q2)
print("\nQuestions 2. Percentage of entries from international students:",str(cur.fetchone()[0]) + "%")



# -------------------------------------------------------------------------------------------------------
#   Questions 3:
# -------------------------------------------------------------------------------------------------------

'''
How many entries report their GPA, GRE, GRE V and GRE AW
'''

print("\n--- Number of applicants who provided each metric ---")
q3_counts = """
SELECT
    COUNT(gpa) AS gpa_count,
    COUNT(gre) AS gre_count,
    COUNT(gre_v) AS gre_v_count,
    COUNT(gre_aw) AS gre_aw_count
FROM applicants;
"""
cur.execute(q3_counts)
gpa_count, gre_count, gre_v_count, gre_aw_count = cur.fetchone()
print(f"GPA provided: {gpa_count}")
print(f"GRE provided: {gre_count}")
print(f"GRE V provided: {gre_v_count}")
print(f"GRE AW provided: {gre_aw_count}")


"""
Question 3: What is the average GPA, GRE, GRE V, GRE AW of applicants who provide these metrics?
"""
print("\n Question 3. Average GPA, GRE, GRE V, and GRE AW (excluding missing values):")
q3 = """
SELECT
    ROUND(AVG(gpa), 2) AS avg_gpa,
    ROUND(AVG(gre), 2) AS avg_gre,
    ROUND(AVG(gre_v), 2) AS avg_gre_v,
    ROUND(AVG(gre_aw), 2) AS avg_gre_aw
FROM applicants;
"""
cur.execute(q3)
avg_gpa, avg_gre, avg_gre_v, avg_gre_aw = cur.fetchone()
print(f"Average GPA: {avg_gpa}")
print(f"Average GRE Total: {avg_gre}")
print(f"Average GRE Verbal: {avg_gre_v}")
print(f"Average GRE AW: {avg_gre_aw}")


cur.close()
conn.close()