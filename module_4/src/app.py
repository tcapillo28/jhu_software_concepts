import re
from flask import Flask, render_template
import src.state as state
from src.query_data import get_full_output
import src.load_data as load_data


def create_app(testing=False):
    """
    Factory function required by pytest.
    Creates a fresh Flask app instance for each test.
    """
    app = Flask(__name__)
    app.config["TESTING"] = testing

    register_routes(app)
    return app


def register_routes(app):
    """
    Register all Flask routes for Module 4.
    """

    # ---------------------------------------------------------
    # Main Analysis Page
    # ---------------------------------------------------------
    @app.route("/")
    def index():
        """
        Render the analysis page with tiles.
        """
        full_text = get_full_output()

        # Split into tiles based on "Question X"
        tiles = re.split(r'\n(?=Question\s+\d+)', full_text.strip())

        parsed_tiles = []
        for block in tiles:
            lines = block.strip().split("\n", 1)
            question = lines[0].strip()
            answer = lines[1].strip() if len(lines) > 1 else ""
            parsed_tiles.append({"question": question, "answer": answer})

        return render_template("index.html", tiles=parsed_tiles)

    # ---------------------------------------------------------
    # Pull Data Button (API)
    # ---------------------------------------------------------
    @app.post("/pull-data")
    def pull_data_api():
        """
        API endpoint triggered by the Pull Data button.
        Tests patch load_rows() to return fake scraped rows.
        """
        if state.is_busy():
            return {"busy": True}, 409

        # Mark busy
        state.set_busy(True)

        # Tests patch this → returns fake rows
        rows = load_data.load_rows()
        load_data.insert_rows(rows)

        # Mark not busy
        state.set_busy(False)

        return {"ok": True}, 200

    # ---------------------------------------------------------
    # Update Analysis Button (API)
    # ---------------------------------------------------------
    @app.post("/update-analysis")
    def update_analysis_api():
        """
        API endpoint triggered by the Update Analysis button.
        """
        if state.is_busy():
            return {"busy": True}, 409

        return {"ok": True}, 200

    @app.get("/analysis")
    def analysis_page():
        full_text = get_full_output()

        tiles = re.split(r'\n(?=Question\s+\d+)', full_text.strip())
        parsed_tiles = []
        for block in tiles:
            lines = block.strip().split("\n", 1)
            question = lines[0].strip()
            answer = lines[1].strip() if len(lines) > 1 else ""
            parsed_tiles.append({"question": question, "answer": answer})

        return render_template("index.html", tiles=parsed_tiles)
# ---------------------------------------------------------
# Run the app normally (not used in pytest)
# ---------------------------------------------------------
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)