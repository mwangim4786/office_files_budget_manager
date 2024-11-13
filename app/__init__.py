#!/usr/bin/python3
"""

"""


from flask import Flask
from flask_font_awesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)


app.config['SECRET_KEY'] = '15363711818daf0f83459c25f7017a90'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lite_storage.db'


db = SQLAlchemy(app)
fa = FontAwesome(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # handles sessions
login_manager.login_view = 'login' # login view - function name for the route login
login_manager.login_message_category = 'info'


# from app import routes
from app.views.users.routes import users
from app.views.about.routes import about
# from app.views.main.routes import main
from app.views.payment.routes import payments
from app.views.budget.routes import budgetz
from app.views.files.routes import filez
from app.views.transactions.routes import transactionz

app.register_blueprint(users)
app.register_blueprint(about)
# app.register_blueprint(main)
app.register_blueprint(payments)
app.register_blueprint(budgetz)
app.register_blueprint(filez)
app.register_blueprint(transactionz)
