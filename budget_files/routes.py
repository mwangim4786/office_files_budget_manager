#!/usr/bin/python3

from budget_files import app

@app.route("/")
def hello():
    return "Hello world!"