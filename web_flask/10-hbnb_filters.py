#!/usr/bin/python3
"""Start web application using Flask
Use the routes: /hbnb_filters: HBNB HTML page filter
"""
from models import storage
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Display the HBNB HTML filters page"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """Remove the present SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
