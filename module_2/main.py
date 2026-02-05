import time
from scrape import scrape_data, save_data
from clean import load_data, clean_data


def main():

    start_time = time.time()

    # -----------------------------
    # 1. SCRAPE RAW DATA (Enter the number of pages. Each page has ~20 entries)
    # -----------------------------
    print("Starting GradCafe scraping...")
    raw_data = scrape_data(pages=1500)
    save_data(raw_data, "saved_data.json")

    # -----------------------------
    # 2. LOAD RAW DATA
    # -----------------------------
    print("\nLoading saved data...")
    loaded_raw = load_data("saved_data.json")

    # -----------------------------
    # 3. CLEAN DATA
    # -----------------------------
    print("Cleaning data...")
    cleaned = clean_data(loaded_raw)

    # -----------------------------
    # 4. SAVE CLEANED DATA
    # -----------------------------
    save_data(cleaned, "applicant_data.json")

    # -----------------------------
    # 5. SUMMARY + RUNTIME
    # -----------------------------
    end_time = time.time()
    print("\nPipeline complete.")
    print(f"Raw entries scraped: {len(raw_data)}")
    print(f"Cleaned entries saved: {len(cleaned)}")
    print(f"Total runtime: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()