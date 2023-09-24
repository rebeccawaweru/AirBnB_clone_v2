#!/usr/bin/python3
"""Start web application using Flask
Use routes: /states & /states/<id> to render
HTML pages
"""
from models import storage
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """Display HTML page containing list of States"""
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Display HTML page with specific info about <id>
    Checks if the <id> exists"""
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown(exc):
    """Remove the present SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
