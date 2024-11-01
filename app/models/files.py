#!/usr/bin/python3
"""

"""

from app import db

class Files(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_no = db.Column(db.String(20), nullable=False)
    file_name = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(300), nullable=False)
    file_fee = db.Column(db.Integer, nullable=False)
    transactions = db.relationship('Transaction', backref='file_no', lazy=True)
    
    def __repr__(self):
        return f"File('{self.id}', '{self.file_no}', '{self.file_name}', '{self.subject}', '{self.file_fee}')"
