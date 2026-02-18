from flask import Flask, render_template, redirect, url_for, request
from src.query_data import get_full_output
import re
import threading
import time
app = Flask(__name__)

# ---------------------------------------------------------
# Pytest needs a way to create a fresh Flask app instance
# for every test
# ---------------------------------------------------------
def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing

    register_routes(app)
    return app


# ---------------------------------------------------------
# Background scraper runner
# ---------------------------------------------------------

# Track whether scraping is running (busy state)
scrape_running = False


def run_scraper():
    global scrape_running
    scrape_running = True

    # Import your module 2 scraper here
    from scrape import scrape_data, save_data

    try:
        # Scrape new data (you can adjust pages or logic)
        new_entries = scrape_data(pages=1)
        save_data(new_entries)
    finally:
        scrape_running = False

# ---------------------------------------------------------
# Route Registration Wrapper
# ---------------------------------------------------------
def register_routes(app):

    # -------------------------------
    # Main Analysis Page
    # -------------------------------
    @app.route("/")
    def index():
        full_text = get_full_output()

        # Split into tiles based on "Question X"
        tiles = re.split(r'\n(?=Question\s+\d+)', full_text.strip())

        # Clean each tile: first line = question, rest = answer
        parsed_tiles = []
        for block in tiles:
            lines = block.strip().split("\n", 1)
            question = lines[0].strip()
            answer = lines[1].strip() if len(lines) > 1 else ""
            parsed_tiles.append({"question": question, "answer": answer})

        message = request.args.get("message", "")

        return render_template("index.html", tiles=parsed_tiles)
    # -------------------------------
    # Pull Data Button Route
    # -------------------------------
    @app.route("/pull_data")
    def pull_data():
        global scrape_running

        if scrape_running:
            return redirect(url_for("index", message="A data pull is already running. Please wait."))

        # Start scraper in background thread
        thread = threading.Thread(target=run_scraper)
        thread.start()

        return redirect(url_for("index", message="Pulling new data from GradCafe… This may take a moment."))

    # -------------------------------
    # Update Analysis Button Route
    # -------------------------------
    @app.route("/update_analysis")
    def update_analysis():
        global scrape_running

        if scrape_running:
            return redirect(url_for("index", message="Cannot update analysis while data is being pulled."))

        # Re-run your analysis logic here
        tiles = get_full_output()

        return redirect(url_for("index", message="Analysis updated with the latest data."))


# ---------------------------------------------------------
# Main Analysis Page
# ---------------------------------------------------------

@app.route("/")
def index():
    full_text = get_full_output()

    # Split into tiles based on "Question X"
    tiles = re.split(r'\n(?=Question\s+\d+)', full_text.strip())

    # Clean each tile: first line = question, rest = answer
    parsed_tiles = []
    for block in tiles:
        lines = block.strip().split("\n", 1)
        question = lines[0].strip()
        answer = lines[1].strip() if len(lines) > 1 else ""
        parsed_tiles.append({"question": question, "answer": answer})
    message = request.args.get("message", "")  # <--- NEW

    return render_template("index.html", tiles=parsed_tiles)

# ---------------------------------------------------------
# Pull Data Button Route
# ---------------------------------------------------------

@app.route("/pull_data")
def pull_data():
    global scrape_running

    if scrape_running:
        return redirect(url_for("index", message="A data pull is already running. Please wait."))

    # Start scraper in background thread
    thread = threading.Thread(target=run_scraper)
    thread.start()

    return redirect(url_for("index", message="Pulling new data from GradCafe… This may take a moment."))

# ---------------------------------------------------------
# Update Analysis Button Route
# ---------------------------------------------------------

@app.route("/update_analysis")
def update_analysis():
    global scrape_running

    if scrape_running:
        return redirect(url_for("index", message="Cannot update analysis while data is being pulled."))

    # Re-run your analysis logic here
    tiles = get_full_output()   # whatever function builds your analysis tiles

    return redirect(url_for("index", message="Analysis updated with the latest data."))

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)


