#!/usr/bin/python3
"""Script that start web application using Flask
Use the route - /cities_by_states
Returns a html page with list of all states and related cities
"""
from models import storage
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """Display a HTML page with list of states
    and related cities"""
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the present SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
