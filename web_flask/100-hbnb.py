#!/usr/bin/python3
"""Start web application using Flask
Use route: '/hbnb' home
"""
from models import storage
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays the HBNB HTML filters page"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    places = storage.all("Place")
    return render_template("100-hbnb.html",
                           states=states, amenities=amenities, places=places)
