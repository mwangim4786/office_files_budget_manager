#!/usr/bin/python3
"""

"""

from app import app, db
from app.models import users, budget, files

class Transaction(db.Model):
    __tablename__ = 'transactions_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    # phone_no = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(users.Users.id), nullable=False)
    budget = db.Column(db.Integer, db.ForeignKey(budget.Budget.id), nullable=False)
    file = db.Column(db.String(20), db.ForeignKey(files.Files.file_no), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    narration = db.Column(db.String(200),nullable=True)
    trans_date = db.Column(db.DateTime(), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    merchant_req_id = db.Column(db.String(40),nullable=True)
    mpesa_ref = db.Column(db.String(20),nullable=True)

    def __repr__(self):
        return f"Transaction('{self.transaction_id}', '{self.amount}', '{self.trans_date}', '{self.status}', '{self.merchant_req_id}', '{self.mpesa_ref}')"
