from . import misc
from flask import render_template

@misc.route("/")
def homepage():
    return render_template("index.html")