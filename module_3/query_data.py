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


"""
Inspect available terms
"""
# Show distinct terms (to demonstrate data validation) with out having to use SQL shell
print("\n--- Distinct Terms in Dataset ---")
q_terms = """
SELECT DISTINCT term
FROM applicants
ORDER BY term;
"""
cur.execute(q_terms)
terms = cur.fetchall()
for t in terms:
    print(t[0])



"""
QUESTION 1: How many entries do you have in your database who have applied for Fall 2025?
"""
q1 = """
SELECT COUNT(*)
FROM applicants
WHERE term = 'Fall 2025';
"""


cur.execute(q1)
print("1. Number of Fall 2025 applicants:", cur.fetchone()[0])

cur.close()
conn.close()