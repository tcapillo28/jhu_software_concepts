from flask import Flask, render_template, redirect, url_for, request, jsonify
from src.query_data import get_full_output, get_static_output
import src.scrape as scrape_module
import src.load_data as load_module
import re
import threading

# Note to run app.py python src/app.py

# ---------------------------------------------------------
# App Factory (Module 4 requirement)
# ---------------------------------------------------------
def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing

    app.scrape_running = False # Module 4 busy-state flag (tests rely on this)

    register_routes(app)
    return app

# ---------------------------------------------------------
# Route Registration Wrapper
# ---------------------------------------------------------

def register_routes(app):
    # Module-3 scrape state
    scrape_running = False

    def run_scraper():
        nonlocal scrape_running
        scrape_running = True

        try:
            new_entries = scrape_data(pages=1)

        finally:
            scrape_running = False

    # -----------------------------------------------------
    # Main Analysis Page
    # -----------------------------------------------------
    @app.route("/")
    def index():
        # Default to static for Module 4 tests
        mode = request.args.get("mode", "static")

        if mode == "real":
            full_text = get_full_output()
        else:
            full_text = get_static_output()

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
        return render_template("index.html", tiles=parsed_tiles, message=message)

    # ---------------------------------------------------------
    # Static instance of analysis page for module 4
    # ---------------------------------------------------------

    @app.route("/analysis")
    def analysis():
        """
        Render the main analysis dashboard page.

        This route serves the HTML page that displays the analysis results along
        with the required Module 4 interface elements. The page includes:
        - The visible title text “Analysis”.
        - The “Pull Data” and “Update Analysis” buttons used to trigger POST routes.
        - The rendered analysis text, which defaults to the static output in
          Module 4 (via index()), ensuring predictable formatting for tests.

        The returned HTML is what the test suite inspects to verify that:
        - The page loads successfully with HTTP 200.
        - At least one “Answer:” label appears in the rendered analysis.
        - Any percentages shown are formatted with exactly two decimal places.

        Returns:
            Response: A fully rendered HTML page containing the analysis dashboard.
        """

        return index()

    # ---------------------------------------------------------
    # Pull Data Button Route
    # ---------------------------------------------------------

    @app.route("/pull_data")
    def pull_data():
        nonlocal scrape_running

        if scrape_running:
            return redirect(url_for("index", message="A data pull is already running. Please wait."))

        # Start scraper in background thread
        thread = threading.Thread(target=run_scraper)
        thread.start()

        return redirect(url_for("index", message="Pulling new data from GradCafe… This may take a moment."))

    # ---------------------------------------------------------
    # Update Analysis Button Route
    # ---------------------------------------------------------

    @app.route("/update_analysis", methods=["GET"])
    def update_analysis():
        nonlocal scrape_running

        if scrape_running:
            return redirect(url_for("index", message="Cannot update analysis while data is being pulled."))

        try:
            get_full_output()
            return redirect(url_for("index", message="Analysis updated with the latest data."))
        except Exception as e:
            return f"Error: {str(e)}", 500

    # ---------------------------------------------------------
    # Module 4 POST routes (these are what your tests expect)
    # ---------------------------------------------------------

    @app.post("/pull_data")
    def pull_data_api():
        if app.scrape_running:
            return jsonify({"busy": True}), 409

        app.scrape_running = True

        rows = scrape_module.scrape_data()  # mocked correctly
        load_module.load_data(rows)  # mocked correctly

        app.scrape_running = False
        return jsonify({"ok": True}), 200

    @app.post("/update_analysis")
    def update_analysis_api():
        if app.scrape_running:
            return jsonify({"busy": True}), 409

        try:
            result = get_full_output()
            return jsonify({"analysis": result}), 200
        except Exception as e:
            return f"Error: {str(e)}", 500


# ---------------------------------------------------------
# Run Server (Module 3 behavior)
# ---------------------------------------------------------

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)