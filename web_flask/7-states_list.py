#!/usr/bin/python3
"""Script that starts a Flask web application
use storage for fetching data from the storage engine
use routes - '/states_list'
"""
from models import storage
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def list_states():
    """Open the list of all the states"""
    states = storage.all("State")
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def tear_down(exc):
    """Remove the present SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
