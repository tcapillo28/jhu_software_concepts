# Module_2: Web scrapping 
Tonya Capillo
JHED ID:
Due Feb 1, 2026 11:59 PM EST

Project Overview:
This project implements a web scraper that collects recent admissions results from The GradCafe, using urllib3 and BeautifulSoup to parse the data.
The goal is to extract structured applicant information, clean it, and output a formatted JSON dataset.
The scraper is designed to be modular, readable, and compliant with the website’s robots.txt rules.

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
### 3. Main:

# Running the program: 


### 4. Limitations:






