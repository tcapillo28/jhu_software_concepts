from flask import Flask, jsonify, render_template, redirect
from . import load_data, scrape, analysis, state

def create_app():
    app = Flask(__name__)
    print("CREATE_APP RAN") # print statement for sanity check of app creation

    @app.get("/")
    def home():
        return redirect("/analysis")

    @app.get("/analysis")
    def analysis_page():
        results = analysis.compute_analysis()
        return render_template("analysis.html", results=results)

    @app.post("/pull-data")
    def pull_data():
        if state.is_busy():
            return jsonify({"error": "busy"}), 409

        state.set_busy(True)
        rows = scrape.load_rows()       # will be mocked in tests
        load_data.insert_rows(rows)
        state.set_busy(False)

        return jsonify({"ok": True}), 200

    @app.post("/update-analysis")
    def update_analysis():
        if state.is_busy():
            return jsonify({"error": "busy"}), 409

        results = analysis.compute_analysis()
        return jsonify({"analysis": results}), 200

    return app
