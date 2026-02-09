# Module_3: Database Queries
Tonya Capillo | JHED ID: 174BAB | Due Feb 8, 2026 11:59 PM EST 
SSH url: git@github.com:tcapillo28/jhu_software_concepts.git

Project Overview:
This project uses two Python scripts — load_data.py and query_data.py — to load applicant data into a PostgreSQL database (dname: gradcafe) and then answer a series of analytical questions using SQL.
- load_data.py reads the provided JSON dataset provided by the professor (llm_extened_applicant_Data.json from Liv) and inserts all applicant records into the applicants table. This script is run once at the beginning to populate the database.
- query_data.py connects to the same PostgreSQL database and executes a sequence of SQL queries, each corresponding to one of the assignment questions. The script prints the results in a clear, labeled format.
Together, these scripts demonstrate the full workflow of:
- Loading structured data into a relational database
- Validating the dataset
- Running SQL queries programmatically
- Producing clean, interpretable outputs


# Running the program:
## Creating database and querying data: 
First connect to database and run load_Data.py followed by query_data.py
1. Database Connection Details
Both load_data.py and query_data.py connect to the same PostgreSQL database using the following parameters:
- dbname: gradcafe
- user: postgres
- password: 2828
- host: localhost
- port: 5432
These values are hard‑coded in each script and must match your local PostgreSQL configuration.
The database must be running before executing either script.

2. Running load_data.py
This script loads the applicant dataset into the PostgreSQL database. 
It reads the JSON file provided by the professor llm_extend_applicant_data.json (renamed to llm_extend_applicant_data_PROVIDED.json)
Run the script from PyCharm or command line: python load_data.py
- Connects to the gradcafe database
- Creates the applicants table if it does not already exist
- Reads the JSON file
- Inserts each applicant record into the database

3. Running query_data.py
Once the database is populated, run this script to execute all assignment queries.
Run the script from PyCharm or command line: python query_data.py
- Connects to the same gradcafe database
- Runs each SQL query (Questions 1–9) and a few additional questions

Include: did not review shared input file to make sure the spelling of program and 

## Flask Webpage



# Limitations
1. LLM Normalization Inconsistencies: 
The dataset includes two LLM‑generated fields — llm_generated_university and llm_generated_program — which attempt to standardize messy scraped text.
While these fields are generally consistent, the LLM is not perfect and may produce slight variations in naming
(e.g., “MIT” vs. “Massachusetts Institute of Technology,” or “CS” vs. “Computer Science”).
Because of this, SQL filters that rely on exact string matching may undercount or miss certain entries. 
A more robust pipeline would include canonical mapping, fuzzy matching, or post‑processing rules to unify these values.
- For the purposes of this assignment, I used the LLM‑generated values as‑is
- In the future iterations should validate and consolidate these fields to ensure complete coverage

2. Raw Scraped Fields Are Noisy and Inflate Counts
The original program field is significantly noisier than the LLM‑generated fields. 
It often contains concatenated text, abbreviations, partial university names, and inconsistent formatting. 
When substring matching (e.g., ILIKE '%Computer%' or ILIKE '%MIT%') is applied to this raw field, many additional entries are matched
— including cases where the keyword appears incidentally or as part of a longer, messy string. 
As a result, the raw‑field version of Question 8 (Question 9) produced a much higher count (25) compared to the LLM‑based version (11). 
This demonstrates how unstandardized text can inflate results and highlights the importance of normalization in data cleaning pipelines.

