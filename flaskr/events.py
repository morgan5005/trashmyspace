from flask import Flask
from flask import Blueprint
from flask import render_template

ev = Blueprint("events", __name__)

@ev.route('/')
def index():
    return render_template("events/index.html")


