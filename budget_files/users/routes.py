#!/usr/bin/python3

from flask import Blueprint

users = Blueprint('users', __name__)

@users.route("/users")
def user():
    return "Users Page."