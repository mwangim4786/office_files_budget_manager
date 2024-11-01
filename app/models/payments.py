#!/usr/bin/python3
"""

"""

from app import db

class Payment(db.Model):
    __tablename__ = 'payments_table'
    id = db.Column(db.Integer, primary_key=True)
    result_code = db.Column(db.Integer)
    phone_no = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    mpesa_ref = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True))
    merchant_req_id = db.Column(db.String(40),nullable=True)
    
    def __repr__(self):
        return f"Payment('{self.result_code}', '{self.phone_no}', '{self.amount}', '{self.mpesa_ref}', '{self.created_at}', '{self.merchant_req_id}')"
