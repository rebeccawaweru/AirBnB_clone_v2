#!/usr/bin/python3
"""Script that starts a Flask web application
Route '/' - 'Hello HBNB!'
Route '/hbnb' - 'HBNB'
Route '/c/<text>' - Display 'C' followed by value
of text variable
"""
from flask import Flask
app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Display 'HBNB'"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def ctxt(text):
    """Display 'C' + text variable"""
    text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
