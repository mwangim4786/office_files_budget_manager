#!/usr/bin/python3
"""

"""

from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20),  unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    transactions = db.relationship('Transaction', backref='phone', lazy=True) # transaction.phone // Users(current user)
    budgets = db.relationship('Budget', backref='phone', lazy=True) # budget.phone // Users(current user)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone}', '{self.role}', '{self.date}')"
