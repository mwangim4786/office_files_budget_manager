#!/usr/bin/python3
"""

"""

from app import app, db
from datetime import datetime
from app.models import users

class Budget(db.Model):
    __tablename__ = 'budgets_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    budget_id = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    purpose = db.Column(db.String(2000), nullable=False)
    bdgt_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    approved_by = db.Column(db.String(200), nullable=False, default='0')
    user_id = db.Column(db.Integer, db.ForeignKey(users.Users.id), nullable=False)
    transactions = db.relationship('Transaction', backref='budget_id', lazy=True)
    
    def __repr__(self):
        return f"Budget('{self.amount}', '{self.purpose}', '{self.bdgt_name}', '{self.status}', '{self.budget_id}', '{self.approved_by}')"
