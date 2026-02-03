# Module_2: Web scrapping 
Tonya Capillo
JHED ID:
Due Feb 1, 2026 11:59 PM EST

Project Overview:
This project implements a web scraper that collects recent admissions results from The GradCafe, using urllib3 and BeautifulSoup to parse the data.
The goal is to extract structured applicant information, clean it, and output a formatted JSON dataset.
The scraper is designed to be modular, readable, and compliant with the website’s robots.txt rules.

# How to Run the Program:
The following files will extract data from GradCafe and generate a *.json file: main.py, scrape.py, and clean.py
1. Install dependencies: pip install -r requirements.txt
2. Run the pipeline (from project root directory): python main.py
3. This will generate the following files:
   - saved_data.json - raw scraped entries
   - applicant_data.json - cleaned, reformatted dataset
Use applicat_data.json as the input for the LLM standardization step in llm_hosting directory
4. Notes:
   - The scraper includes a hard cap of 30,000 entries, regardless of how many pages you request.
   - If GradCafe runs out of pages, the scraper stops early.
   - The pipeline is modular, so each stage can be run independently if needed. In the file scrape.py, some functions will be moved to clean.py

# Running the LLM Standardizer
After generating applicant_data.json with the scraping and cleaning pipeline, the next step is to standardize program names and university names using a small local LLM. This stage is implemented in the llm_hosting directory and uses a lightweight GGUF model (TinyLlama) through llama-cpp-python.
1. Install LLM dependencies: cd llm_hosting
2. Install required packages: pip install -r requirements.txt
- Note: On Windows, llama-cpp-python requires the Microsoft C++ Build Tools (Desktop Development with C++ workload).
3. A) Run the LLM standardizer (from inside the llm_hosting directory): python app.py --file "applicant_data.json" --stdout > out.json
There are test files: sample.json that can be used to test the LLM standardizer prior to applicant_data.json
3. B) Output file:
  - out.json - final standardized dataset
  - canonical_programs.json — list of accepted program names
  - canonical_universities.json — list of accepted university names
These canonical lists can be updated and expanded to correct systematic LLM errors. I did not change these files.
Note: 




# Compliance
#### robots.txt compliance
Before scraping any data, I retrieved and reviewed the site’s robots.txt file to ensure my scraper adhered to the website’s access policies.
The following content-signal allow content collection for search/indexing purposes but prohibits using the data for AI model training.
This project does not use scraped data for training any AI models. Additional disallow rules apply only to specific bots or specific paths.
This scraper does not allow any restricted path.

#### Explanation of notation description:
User-agent:* applies to all general-purpose crawlers, including this scraper.
Allow:/ explicitly permits access to all publicly available pages on the site.

#### Code used to fetch robots.txt

                import urllib3

                def fetch_robots_txt():
                    http = urllib3.PoolManager()
                    url = "https://www.thegradcafe.com/robots.txt"
                    response = http.request("GET", url)
                    robots = response.data.decode("utf-8")
                    print(robots)
                    return robots

                The file returned:
                    User-agent: *
                    Content-Signal: search=yes, ai-train=no
                    Allow: /

# scrape.py
### 1. Scrapper Description (scrape.py):
This function loops through the specified number of pages, fetches each page’s HTML, parses the admissions table, and accumulates entries into a Python list. A hard cap (max_entries=30000) ensures the scraper never exceeds the assignment’s dataset limit, even if the user accidentally requests too many pages.

1. Sequential pagination
Pages are fetched in order (1, 2, 3, …) until either the requested number of pages is reached or the site stops returning results.

2. Modularity
Each task is handled by a dedicated helper function:
-- _fetch_html() retrieves the raw HTML for a page.
- _parse_table() extracts structured data from the HTML table.
- _fetch_comments() and _fetch_stats() retrieve additional details from each result’s detail page.
- _split_program_and_degree() and _split_decision() normalize text fields.

3. Safety and robustness
- A global counter tracks the number of processed entries.
- The scraper stops early if a page contains no results.
- The 30,000‑entry cap prevents overscraping.
- Each network request includes a user‑agent header to avoid being blocked.

#### 1.1 Parsing the admission table
The _parse_table(html) function uses BeautifulSoup to locate the main results table:
table = soup.find("table")

Rows with fewer than four <td> cells are skipped to avoid malformed entries.
Each row is processed to extract:
- School name
- Program name
- Degree type
- Added‑on date
- Decision status and date
- URL to the detail page

#### 1.2 Extracting comments and stats from detail page(s)
Regex is used to parse GRE/GPA values from unstructured text.
If a result includes a detail page URL, two helper functions are called:
- _fetch_comments(url)
- _fetch_stats(url)
These functions extract:
- Comments
- GPA
- GRE total, verbal, quantitative, and analytical writing
- Citizenship
- Term (e.g., Fall 2024)


#### 1.3 Normalize program and decision fields
Two helper functions clean up text fields:
- _split_program_and_degree()
- _split_decision()
- 
These functions separate combined fields like:
"Computer Science PhD"
"Accepted on 2 Feb 2025"

into structured components.

#### 1.4 Building a structured entry
Each processed row(entry) becomes a dictionary with consistent keys.
A global counter increments for every entry, which helps with debugging and progress tracking.

#### 1.5 Stop conditions
This ensures the scraper behaves predictably and safely.
The scraper stops when:
- The requested number of pages has been reached
- A page returns no results
- The 30,000‑entry cap is reached

#### 1.6 main block
This block allows the file to be run directly as a script for testing or debugging without using main.py. It starts a timer, runs the scraper, saves the data, and prints the time taken for the scrape. This block only runs when the file is executed directly.

# clean.py
Note: Moving the parsing of the admission table to clean.py should be in this file instead of scrape.py (ask grader and professor).  Technically, clean.py is a reformatter, not a cleaner of the dataset. 
#### 2. Cleaning and normalizing entries:
The main function, clean_data(raw_entries), iterates through each scraped entry and constructs a new dictionary with standardized keys and structure.
This ensures every entry has the same format, even when some fields are missing
Each cleaned entry includes:
- school — university name
- program — raw program name extracted from the table
- degree_type — parsed degree (e.g., PhD, MS, MA)
- status — decision status (e.g., Accepted, Rejected, Interview)
- decision_date — normalized date string
- gpa — applicant GPA (if available)
- gre — nested dictionary containing:
- total
- verbal (v)
- quantitative (q)
- analytical writing (aw)
- citizenship — American or International (if detected)
- term — admissions term (e.g., Fall 2024)
- comments — list of comments scraped from the detail page
- url — link to the original GradCafe entry

####  Date Normalization
The helper function _normalize_date() currently returns the date unchanged unless it is missing. This placeholder exists so that future improvements (e.g., adding missing years or converting formats) can be implemented without changing the rest of the pipeline. Some dates contain the month and day but not the year. 

# main.py
### 3. Main program description:
The main.py file serves as the orchestrator for the entire data‑processing pipeline, coordinating the scraping, cleaning, and saving of GradCafe admissions data. It begins by starting a runtime timer, then calls scrape_data() to collect raw entries from the website while respecting the built‑in 30,000‑entry safety cap. The scraped results are saved to saved_data.json and then reloaded with load_data() to ensure the cleaning stage always operates on a stable, reproducible dataset. Next, clean_data() transforms the raw entries into a consistent, structured format suitable for downstream LLM processing and saves the cleaned output as applicant_data.json. Finally, the script prints a summary of the number of entries scraped and cleaned, along with the total runtime. 




### 4. Limitations:
In the applicant_data.json the comments section doesn't return a 'None' or "" and instead returns []. 





