#!/usr/bin/python3


from flask import Flask
app = Flask(__name__)


# from budget_files import routes
from budget_files.users.routes import users
from budget_files.about.routes import about
from budget_files.main.routes import main

app.register_blueprint(users)
app.register_blueprint(about)
app.register_blueprint(main)
