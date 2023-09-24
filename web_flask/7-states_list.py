#!/usr/bin/python3
"""Script that starts a Flask web application
use storage for fetching data from the storage engine
use routes - '/states_list'
"""
from flask import Flask, render_template
import models
from models.state import State
app = Flask(__name__, template_folder='templates')


@app.route("/states_list", strict_slashes=False)
def list_states():
    """Open the list of all the states"""
    states = models.storage.all(State).values()
    return render_template('7-status_list.html', states=states)


@app.teardown_appcontext
def tear_down(error):
    """Remove the present SQLAlchemy Session"""
    models.storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
