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
print("Question 1. Number of Fall 2025 applicants:", cur.fetchone()[0])


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
What are the total number of entries from all distinct citizenship categories
"""


"""
Question 2: What percentage of entries are from international students (not American or Other) (to two decimal places)?
"""


cur.close()
conn.close()