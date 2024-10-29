#!/usr/bin/python3

from flask import Blueprint

about = Blueprint('about', __name__)

@about.route("/about")
def abt():
    return "About Page."