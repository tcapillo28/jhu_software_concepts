"""
    Flask application for the Module 4 analytics dashboard.
    
    This module defines the Flask application factory and all HTTP routes used
    in the assignment. The application provides:
    
    - A redirect from the home page to the analysis page.
    - A page that renders the current analysis results using a Jinja2 template.
    - An endpoint to trigger a data pull (mocked in tests).
    - An endpoint to recompute and return analysis results as JSON.
    
    All data operations (loading, scraping, analysis, and busy‑state tracking)
    are delegated to helper modules inside ``src/``. During testing, these
    functions are patched/mocked, so the Flask routes only orchestrate workflow.
"""
from flask import Flask, jsonify, render_template, redirect
from . import load_data, scrape, analysis, state


def create_app():
    """
        Create and configure the Flask application.

        This function is used by both the real application and the pytest suite.
        It registers all routes and returns a fully configured Flask instance.

        Returns:
            Flask: The configured Flask application.
    """

    app = Flask(__name__)
    print("CREATE_APP RAN") # print statement for sanity check of app creation

    @app.get("/")
    def home():

        """
            Redirect the user to the analysis page.

            Returns:
                Response: A redirect response pointing to ``/analysis``.
        """

        return redirect("/analysis")

    @app.get("/analysis")
    def analysis_page():
        """
        Render the analysis dashboard page.

        This route calls ``analysis.compute_analysis()`` to obtain the
        current computed metrics, then renders them using the
        ``analysis.html`` Jinja2 template.

        Returns:
            Response: Rendered HTML containing the analysis results.
        """

        results = analysis.compute_analysis()
        return render_template("analysis.html", results=results)

    @app.post("/pull-data")
    def pull_data():
        """
        Trigger a data pull and insert new rows.

        This endpoint is used to simulate scraping new data. In the real
        application, ``scrape.load_rows()`` would fetch external data, but
        in Module 4 it is patched during testing to return controlled values.

        Workflow:
            - Reject the request if the system is busy.
            - Mark the system as busy.
            - Load rows (mocked in tests).
            - Insert rows into storage.
            - Mark the system as not busy.

        Returns:
            tuple: A JSON response and HTTP status code.
                - ``{"ok": True}`` with status 200 on success.
                - ``{"error": "busy"}`` with status 409 if already busy.
        """

        if state.is_busy():
            return jsonify({"error": "busy"}), 409

        state.set_busy(True)
        rows = scrape.load_rows()       # will be mocked in tests
        load_data.insert_rows(rows)
        state.set_busy(False)

        return jsonify({"ok": True}), 200

    @app.post("/update-analysis")
    def update_analysis():
        """
        Recompute and return the latest analysis results.

        This endpoint is used by the "Update Analysis" button in the UI.
        It recomputes metrics using ``analysis.compute_analysis()`` and
        returns them as JSON.

        Returns:
            tuple: A JSON response and HTTP status code.
                - ``{"analysis": results}`` with status 200 on success.
                - ``{"error": "busy"}`` with status 409 if a data pull is running.
        """
        if state.is_busy():
            return jsonify({"error": "busy"}), 409

        results = analysis.compute_analysis()
        return jsonify({"analysis": results}), 200

    return app
